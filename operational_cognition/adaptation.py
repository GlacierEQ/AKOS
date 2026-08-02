from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from math import exp
from typing import Iterable, Mapping, Sequence


class AdaptationReason(str, Enum):
    INITIAL_SELECTION = "initial_selection"
    HEALTH_DEGRADED = "health_degraded"
    LATENCY_DEGRADED = "latency_degraded"
    ERROR_BUDGET_EXHAUSTED = "error_budget_exhausted"
    RATE_LIMITED = "rate_limited"
    COST_PRESSURE = "cost_pressure"
    QUEUE_PRESSURE = "queue_pressure"
    RECOVERY_PROBE = "recovery_probe"
    MANUAL_OVERRIDE = "manual_override"


class AdaptationAction(str, Enum):
    KEEP = "keep"
    SWITCH = "switch"
    BACKOFF = "backoff"
    PROBE = "probe"
    BLOCK = "block"


@dataclass(frozen=True)
class RuntimeSignal:
    capability: str
    observed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    healthy: bool = True
    latency_ms: float = 0.0
    success_rate: float = 1.0
    rate_limited: bool = False
    queue_depth: int = 0
    unit_cost: float = 0.0
    confidence: float = 1.0

    def validate(self) -> None:
        if not self.capability.strip():
            raise ValueError("capability must not be empty")
        if self.latency_ms < 0:
            raise ValueError("latency_ms must be non-negative")
        if not 0 <= self.success_rate <= 1:
            raise ValueError("success_rate must be between 0 and 1")
        if self.queue_depth < 0:
            raise ValueError("queue_depth must be non-negative")
        if self.unit_cost < 0:
            raise ValueError("unit_cost must be non-negative")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class AdaptationPolicy:
    minimum_health_score: float = 0.45
    switch_margin: float = 0.08
    target_latency_ms: float = 1_000.0
    maximum_queue_depth: int = 100
    cost_weight: float = 0.10
    latency_weight: float = 0.20
    reliability_weight: float = 0.40
    confidence_weight: float = 0.20
    queue_weight: float = 0.10
    base_interval_seconds: int = 300
    minimum_interval_seconds: int = 60
    maximum_interval_seconds: int = 7_200
    maximum_backoff_seconds: int = 3_600

    def validate(self) -> None:
        if not 0 <= self.minimum_health_score <= 1:
            raise ValueError("minimum_health_score must be between 0 and 1")
        if self.switch_margin < 0:
            raise ValueError("switch_margin must be non-negative")
        if self.target_latency_ms <= 0:
            raise ValueError("target_latency_ms must be positive")
        if self.maximum_queue_depth <= 0:
            raise ValueError("maximum_queue_depth must be positive")
        if self.minimum_interval_seconds <= 0:
            raise ValueError("minimum_interval_seconds must be positive")
        if self.maximum_interval_seconds < self.minimum_interval_seconds:
            raise ValueError("maximum interval must not be below minimum interval")
        if self.maximum_backoff_seconds <= 0:
            raise ValueError("maximum_backoff_seconds must be positive")
        total = (
            self.cost_weight
            + self.latency_weight
            + self.reliability_weight
            + self.confidence_weight
            + self.queue_weight
        )
        if abs(total - 1.0) > 1e-9:
            raise ValueError("adaptation weights must sum to 1.0")


@dataclass(frozen=True)
class RankedCapability:
    capability: str
    score: float
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class AdaptationDecision:
    action: AdaptationAction
    reason: AdaptationReason
    selected_capability: str | None
    previous_capability: str | None
    next_interval_seconds: int
    ranked: tuple[RankedCapability, ...]
    exact_blocker: str | None = None


@dataclass(frozen=True)
class AdaptationReceipt:
    decision: AdaptationDecision
    signal_count: int
    policy_fingerprint: str
    recorded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> Mapping[str, object]:
        return {
            "schema": "glaciereq.akos.adaptation-receipt.v1",
            "recorded_at": self.recorded_at,
            "signal_count": self.signal_count,
            "policy_fingerprint": self.policy_fingerprint,
            "decision": {
                "action": self.decision.action.value,
                "reason": self.decision.reason.value,
                "selected_capability": self.decision.selected_capability,
                "previous_capability": self.decision.previous_capability,
                "next_interval_seconds": self.decision.next_interval_seconds,
                "exact_blocker": self.decision.exact_blocker,
                "ranked": [
                    {
                        "capability": item.capability,
                        "score": item.score,
                        "reasons": list(item.reasons),
                    }
                    for item in self.decision.ranked
                ],
            },
        }


class DynamicAdjustmentEngine:
    """Deterministic adaptive routing with bounded cadence and receipts."""

    def __init__(self, policy: AdaptationPolicy | None = None) -> None:
        self.policy = policy or AdaptationPolicy()
        self.policy.validate()

    def score(self, signal: RuntimeSignal) -> RankedCapability:
        signal.validate()
        policy = self.policy
        reliability = signal.success_rate if signal.healthy else 0.0
        latency = exp(-signal.latency_ms / policy.target_latency_ms)
        queue = max(0.0, 1.0 - signal.queue_depth / policy.maximum_queue_depth)
        cost = 1.0 / (1.0 + signal.unit_cost)
        score = (
            policy.reliability_weight * reliability
            + policy.latency_weight * latency
            + policy.queue_weight * queue
            + policy.cost_weight * cost
            + policy.confidence_weight * signal.confidence
        )
        reasons: list[str] = []
        if not signal.healthy:
            score *= 0.25
            reasons.append("unhealthy")
        if signal.rate_limited:
            score *= 0.20
            reasons.append("rate_limited")
        if signal.latency_ms > policy.target_latency_ms:
            reasons.append("latency_above_target")
        if signal.queue_depth > policy.maximum_queue_depth:
            reasons.append("queue_above_limit")
        if signal.success_rate < policy.minimum_health_score:
            reasons.append("success_below_threshold")
        return RankedCapability(
            signal.capability,
            round(max(0.0, min(score, 1.0)), 6),
            tuple(reasons),
        )

    def decide(
        self,
        signals: Iterable[RuntimeSignal],
        *,
        current_capability: str | None = None,
        consecutive_failures: int = 0,
        activity_pressure: float = 0.0,
        manual_override: str | None = None,
    ) -> AdaptationDecision:
        if consecutive_failures < 0:
            raise ValueError("consecutive_failures must be non-negative")
        if not 0 <= activity_pressure <= 1:
            raise ValueError("activity_pressure must be between 0 and 1")
        signal_list = list(signals)
        ranked = tuple(
            sorted(
                (self.score(signal) for signal in signal_list),
                key=lambda item: (-item.score, item.capability),
            )
        )
        signal_names = {item.capability for item in ranked}
        interval = self._next_interval(
            activity_pressure=activity_pressure,
            consecutive_failures=consecutive_failures,
        )
        if manual_override is not None:
            if manual_override not in signal_names:
                return AdaptationDecision(
                    AdaptationAction.BLOCK,
                    AdaptationReason.MANUAL_OVERRIDE,
                    None,
                    current_capability,
                    interval,
                    ranked,
                    "manual override capability has no current runtime signal",
                )
            return AdaptationDecision(
                AdaptationAction.KEEP
                if manual_override == current_capability
                else AdaptationAction.SWITCH,
                AdaptationReason.MANUAL_OVERRIDE,
                manual_override,
                current_capability,
                interval,
                ranked,
            )
        if not ranked:
            return AdaptationDecision(
                AdaptationAction.BLOCK,
                AdaptationReason.HEALTH_DEGRADED,
                None,
                current_capability,
                interval,
                ranked,
                "no runtime signals were supplied",
            )
        best = ranked[0]
        current = next(
            (item for item in ranked if item.capability == current_capability),
            None,
        )
        if best.score < self.policy.minimum_health_score:
            return AdaptationDecision(
                AdaptationAction.BACKOFF,
                AdaptationReason.ERROR_BUDGET_EXHAUSTED,
                current_capability,
                current_capability,
                interval,
                ranked,
                "all observed capabilities are below the health threshold",
            )
        if current is None:
            return AdaptationDecision(
                AdaptationAction.SWITCH,
                AdaptationReason.INITIAL_SELECTION,
                best.capability,
                current_capability,
                interval,
                ranked,
            )
        if (
            best.capability != current.capability
            and best.score - current.score >= self.policy.switch_margin
        ):
            return AdaptationDecision(
                AdaptationAction.SWITCH,
                self._switch_reason(signal_list, current.capability),
                best.capability,
                current.capability,
                interval,
                ranked,
            )
        return AdaptationDecision(
            AdaptationAction.KEEP,
            AdaptationReason.RECOVERY_PROBE,
            current.capability,
            current.capability,
            interval,
            ranked,
        )

    def receipt(
        self,
        decision: AdaptationDecision,
        *,
        signal_count: int,
    ) -> AdaptationReceipt:
        return AdaptationReceipt(
            decision=decision,
            signal_count=signal_count,
            policy_fingerprint=self._policy_fingerprint(),
        )

    def _next_interval(
        self,
        *,
        activity_pressure: float,
        consecutive_failures: int,
    ) -> int:
        policy = self.policy
        activity_interval = int(
            policy.base_interval_seconds
            - activity_pressure
            * (policy.base_interval_seconds - policy.minimum_interval_seconds)
        )
        failure_backoff = min(
            policy.maximum_backoff_seconds,
            policy.base_interval_seconds * (2 ** min(consecutive_failures, 8)),
        )
        interval = max(
            activity_interval,
            failure_backoff if consecutive_failures else 0,
        )
        return max(
            policy.minimum_interval_seconds,
            min(interval, policy.maximum_interval_seconds),
        )

    @staticmethod
    def _switch_reason(
        signals: Sequence[RuntimeSignal],
        current_capability: str,
    ) -> AdaptationReason:
        current = next(
            signal for signal in signals if signal.capability == current_capability
        )
        if current.rate_limited:
            return AdaptationReason.RATE_LIMITED
        if not current.healthy or current.success_rate < 0.5:
            return AdaptationReason.HEALTH_DEGRADED
        if current.queue_depth > 100:
            return AdaptationReason.QUEUE_PRESSURE
        if current.latency_ms > 1_000:
            return AdaptationReason.LATENCY_DEGRADED
        return AdaptationReason.COST_PRESSURE

    def _policy_fingerprint(self) -> str:
        values = (
            self.policy.minimum_health_score,
            self.policy.switch_margin,
            self.policy.target_latency_ms,
            self.policy.maximum_queue_depth,
            self.policy.cost_weight,
            self.policy.latency_weight,
            self.policy.reliability_weight,
            self.policy.confidence_weight,
            self.policy.queue_weight,
            self.policy.base_interval_seconds,
            self.policy.minimum_interval_seconds,
            self.policy.maximum_interval_seconds,
            self.policy.maximum_backoff_seconds,
        )
        return "|".join(str(value) for value in values)
