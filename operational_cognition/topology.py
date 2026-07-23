from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable

from .engine import OperationClass, WorkItem


class SystemRole(str, Enum):
    SOURCE = "source"
    CANONICAL = "canonical"
    CONTROL_PLANE = "control_plane"
    EXECUTION_PLANE = "execution_plane"
    RECEIPT_PLANE = "receipt_plane"
    MIRROR = "mirror"


class RouteState(str, Enum):
    DISCOVER = "discover"
    READY = "ready"
    EXTEND_EXISTING = "extend_existing"
    BLOCKED = "blocked"


class ProposalKind(str, Enum):
    PRIVATE_WORKFLOW = "private_workflow"
    NEW_RUNNER = "new_runner"
    NEW_CONTROL_PLANE = "new_control_plane"
    CATALOG_ACTION = "catalog_action"
    ADAPTER = "adapter"
    ROUTE_BINDING = "route_binding"


@dataclass(frozen=True)
class SystemNode:
    name: str
    roles: frozenset[SystemRole]
    systems: frozenset[str]
    operations: frozenset[OperationClass]
    active: bool = True
    private: bool = False
    authoritative_for: frozenset[str] = frozenset()
    source_ref: str | None = None

    def supports(self, work: WorkItem) -> bool:
        return (
            self.active
            and work.operation in self.operations
            and (work.target_system in self.systems or "*" in self.systems)
        )

    def has_role(self, role: SystemRole) -> bool:
        return role in self.roles


@dataclass(frozen=True)
class ArchitectureSnapshot:
    snapshot_id: str
    source_refs: tuple[str, ...]
    nodes: tuple[SystemNode, ...]
    verified: bool
    recorded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def validate(self) -> None:
        if not self.snapshot_id.strip():
            raise ValueError("architecture snapshot_id is required")
        if not self.source_refs:
            raise ValueError("architecture snapshot requires authoritative source refs")
        if any(not source.strip() for source in self.source_refs):
            raise ValueError("architecture source refs must not be empty")
        names = [node.name for node in self.nodes]
        if len(names) != len(set(names)):
            raise ValueError("architecture node names must be unique")
        if not any(node.active for node in self.nodes):
            raise ValueError("architecture snapshot has no active nodes")

    def nodes_for_role(self, role: SystemRole) -> tuple[SystemNode, ...]:
        return tuple(
            node for node in self.nodes if node.active and node.has_role(role)
        )

    def supporting_nodes(
        self,
        role: SystemRole,
        work: WorkItem,
    ) -> tuple[SystemNode, ...]:
        return tuple(
            node
            for node in self.nodes_for_role(role)
            if node.supports(work)
        )


@dataclass(frozen=True)
class ExecutionRoute:
    state: RouteState
    reason: str
    source_node: str | None = None
    execution_node: str | None = None
    control_node: str | None = None
    receipt_node: str | None = None
    next_action: str | None = None
    exact_blocker: str | None = None

    @property
    def path(self) -> tuple[str, ...]:
        return tuple(
            value
            for value in (
                self.source_node,
                self.control_node,
                self.execution_node,
                self.receipt_node,
            )
            if value
        )


@dataclass(frozen=True)
class InfrastructureDecision:
    allowed: bool
    reason: str
    required_action: str
    route: ExecutionRoute


class SystemFirstOrchestrator:
    """Resolve existing architecture before diagnosing absence or building anew."""

    def resolve(
        self,
        work: WorkItem,
        snapshot: ArchitectureSnapshot | None,
    ) -> ExecutionRoute:
        if snapshot is None or not snapshot.verified:
            return ExecutionRoute(
                state=RouteState.DISCOVER,
                reason="authoritative_topology_required",
                next_action=(
                    "inspect canonical manifests, execution catalogs, workflows, "
                    "open pull requests, and receipt stores before declaring a blocker"
                ),
            )

        try:
            snapshot.validate()
        except ValueError as exc:
            return ExecutionRoute(
                state=RouteState.BLOCKED,
                reason="invalid_architecture_snapshot",
                exact_blocker=str(exc),
            )

        execution_nodes = snapshot.supporting_nodes(
            SystemRole.EXECUTION_PLANE,
            work,
        )
        control_nodes = snapshot.nodes_for_role(SystemRole.CONTROL_PLANE)
        receipt_nodes = snapshot.nodes_for_role(SystemRole.RECEIPT_PLANE)
        source_nodes = snapshot.supporting_nodes(SystemRole.SOURCE, work)
        canonical_nodes = snapshot.nodes_for_role(SystemRole.CANONICAL)

        source = self._prefer_authoritative(
            source_nodes or canonical_nodes,
            work.target_system,
        )
        control = self._first(control_nodes)
        receipt = self._first(receipt_nodes)

        if execution_nodes:
            execution = self._prefer_authoritative(
                execution_nodes,
                work.target_system,
            )
            if receipt is None:
                return ExecutionRoute(
                    state=RouteState.BLOCKED,
                    reason="receipt_plane_missing",
                    source_node=source.name if source else None,
                    execution_node=execution.name if execution else None,
                    control_node=control.name if control else None,
                    exact_blocker=(
                        "an execution path exists but no active receipt plane is bound"
                    ),
                )
            return ExecutionRoute(
                state=RouteState.READY,
                reason="existing_route_resolved",
                source_node=source.name if source else None,
                execution_node=execution.name if execution else None,
                control_node=control.name if control else None,
                receipt_node=receipt.name,
                next_action=(
                    f"route the bounded workload through {execution.name}; preserve "
                    f"policy in {control.name if control else 'the canonical control plane'} "
                    f"and publish the immutable receipt to {receipt.name}"
                ),
            )

        existing_execution_planes = snapshot.nodes_for_role(
            SystemRole.EXECUTION_PLANE
        )
        if existing_execution_planes:
            execution = self._prefer_authoritative(
                existing_execution_planes,
                work.target_system,
            )
            return ExecutionRoute(
                state=RouteState.EXTEND_EXISTING,
                reason="execution_plane_exists_but_route_is_unregistered",
                source_node=source.name if source else None,
                execution_node=execution.name if execution else None,
                control_node=control.name if control else None,
                receipt_node=receipt.name if receipt else None,
                next_action=(
                    f"extend {execution.name} with one bounded catalog action, adapter, "
                    "or route binding; do not create a private workflow or replacement runner"
                ),
            )

        return ExecutionRoute(
            state=RouteState.BLOCKED,
            reason="no_execution_plane_in_verified_topology",
            source_node=source.name if source else None,
            control_node=control.name if control else None,
            receipt_node=receipt.name if receipt else None,
            exact_blocker=(
                "the verified architecture contains no active execution plane"
            ),
        )

    def evaluate_proposal(
        self,
        work: WorkItem,
        snapshot: ArchitectureSnapshot | None,
        proposal: ProposalKind,
    ) -> InfrastructureDecision:
        route = self.resolve(work, snapshot)

        if route.state == RouteState.DISCOVER:
            return InfrastructureDecision(
                allowed=False,
                reason="discovery_precedes_infrastructure_change",
                required_action=route.next_action or "discover existing architecture",
                route=route,
            )

        if proposal == ProposalKind.PRIVATE_WORKFLOW and route.execution_node:
            return InfrastructureDecision(
                allowed=False,
                reason="private_workflow_duplicates_existing_execution_plane",
                required_action=(
                    f"dispatch metadata-only work to {route.execution_node}"
                ),
                route=route,
            )

        if proposal in {
            ProposalKind.NEW_RUNNER,
            ProposalKind.NEW_CONTROL_PLANE,
        } and route.state in {RouteState.READY, RouteState.EXTEND_EXISTING}:
            return InfrastructureDecision(
                allowed=False,
                reason="existing_architecture_must_be_reused",
                required_action=(
                    route.next_action
                    or "bind the workload to the existing architecture"
                ),
                route=route,
            )

        if proposal in {
            ProposalKind.CATALOG_ACTION,
            ProposalKind.ADAPTER,
            ProposalKind.ROUTE_BINDING,
        }:
            allowed = route.state == RouteState.EXTEND_EXISTING
            return InfrastructureDecision(
                allowed=allowed,
                reason=(
                    "bounded_extension_matches_existing_architecture"
                    if allowed
                    else "extension_not_required_for_resolved_route"
                ),
                required_action=(
                    route.next_action
                    if allowed
                    else "use the already resolved route without expansion"
                )
                or "use the resolved route",
                route=route,
            )

        return InfrastructureDecision(
            allowed=route.state == RouteState.BLOCKED,
            reason=(
                "new_infrastructure_requires_verified_absence"
                if route.state == RouteState.BLOCKED
                else "reuse_existing_architecture"
            ),
            required_action=(
                route.exact_blocker
                or route.next_action
                or "use the verified existing route"
            ),
            route=route,
        )

    @staticmethod
    def _first(nodes: Iterable[SystemNode]) -> SystemNode | None:
        return next(iter(nodes), None)

    @staticmethod
    def _prefer_authoritative(
        nodes: Iterable[SystemNode],
        target_system: str,
    ) -> SystemNode | None:
        candidates = tuple(nodes)
        if not candidates:
            return None
        return sorted(
            candidates,
            key=lambda node: (
                target_system in node.authoritative_for,
                target_system in node.systems,
                not node.private,
                node.name,
            ),
            reverse=True,
        )[0]
