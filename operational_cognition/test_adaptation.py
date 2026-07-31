import unittest

from operational_cognition.adaptation import (
    AdaptationAction,
    AdaptationReason,
    DynamicAdjustmentEngine,
    RuntimeSignal,
)


class DynamicAdjustmentEngineTests(unittest.TestCase):
    def test_selects_best_initial_capability(self) -> None:
        engine = DynamicAdjustmentEngine()
        decision = engine.decide(
            [
                RuntimeSignal(capability="slow", latency_ms=2500, success_rate=0.95),
                RuntimeSignal(capability="fast", latency_ms=100, success_rate=0.99),
            ]
        )
        self.assertEqual(decision.action, AdaptationAction.SWITCH)
        self.assertEqual(decision.reason, AdaptationReason.INITIAL_SELECTION)
        self.assertEqual(decision.selected_capability, "fast")

    def test_switches_away_from_rate_limited_capability(self) -> None:
        engine = DynamicAdjustmentEngine()
        decision = engine.decide(
            [
                RuntimeSignal(capability="primary", rate_limited=True),
                RuntimeSignal(capability="fallback", latency_ms=150),
            ],
            current_capability="primary",
        )
        self.assertEqual(decision.action, AdaptationAction.SWITCH)
        self.assertEqual(decision.reason, AdaptationReason.RATE_LIMITED)
        self.assertEqual(decision.selected_capability, "fallback")

    def test_backoff_is_bounded(self) -> None:
        engine = DynamicAdjustmentEngine()
        decision = engine.decide(
            [RuntimeSignal(capability="down", healthy=False, success_rate=0.0)],
            current_capability="down",
            consecutive_failures=20,
        )
        self.assertEqual(decision.action, AdaptationAction.BACKOFF)
        self.assertLessEqual(
            decision.next_interval_seconds,
            engine.policy.maximum_interval_seconds,
        )

    def test_activity_pressure_shortens_interval(self) -> None:
        engine = DynamicAdjustmentEngine()
        quiet = engine.decide(
            [RuntimeSignal(capability="a")], activity_pressure=0.0
        )
        busy = engine.decide(
            [RuntimeSignal(capability="a")], activity_pressure=1.0
        )
        self.assertGreater(quiet.next_interval_seconds, busy.next_interval_seconds)

    def test_manual_override_requires_signal(self) -> None:
        engine = DynamicAdjustmentEngine()
        decision = engine.decide(
            [RuntimeSignal(capability="known")], manual_override="missing"
        )
        self.assertEqual(decision.action, AdaptationAction.BLOCK)
        self.assertIsNotNone(decision.exact_blocker)

    def test_receipt_is_machine_readable(self) -> None:
        engine = DynamicAdjustmentEngine()
        decision = engine.decide([RuntimeSignal(capability="a")])
        receipt = engine.receipt(decision, signal_count=1).as_dict()
        self.assertEqual(receipt["schema"], "glaciereq.akos.adaptation-receipt.v1")
        self.assertEqual(receipt["signal_count"], 1)


if __name__ == "__main__":
    unittest.main()
