from __future__ import annotations

import unittest

from operational_cognition.engine import OperationClass, SourceKind, WorkItem
from operational_cognition.topology import (
    ArchitectureSnapshot,
    ProposalKind,
    RouteState,
    SystemFirstOrchestrator,
    SystemNode,
    SystemRole,
)


ALL_OPERATIONS = frozenset(OperationClass)


def work(target_system: str = "github_actions.private_workload_ci") -> WorkItem:
    return WorkItem(
        work_id="AKOS-TOPOLOGY-001",
        goal="Validate a private AKOS workload",
        target_system=target_system,
        operation=OperationClass.ANALYZE,
        source_kind=SourceKind.PRIVATE_CONNECTED,
        expected_outcome="a receipt-backed test result",
    )


def canonical_snapshot(
    *,
    execution_systems: frozenset[str] = frozenset(
        {"github_actions.private_workload_ci"}
    ),
    include_receipt: bool = True,
    verified: bool = True,
) -> ArchitectureSnapshot:
    nodes = [
        SystemNode(
            name="GlacierEQ/AKOS",
            roles=frozenset({SystemRole.SOURCE, SystemRole.CANONICAL}),
            systems=frozenset({"github_actions.private_workload_ci"}),
            operations=ALL_OPERATIONS,
            private=True,
            authoritative_for=frozenset({"akos_policy"}),
            source_ref="AKOS_MANIFEST.yaml",
        ),
        SystemNode(
            name="GlacierEQ/public-actions-runner-host",
            roles=frozenset({SystemRole.EXECUTION_PLANE}),
            systems=execution_systems,
            operations=ALL_OPERATIONS,
            private=False,
            authoritative_for=frozenset({"github_actions.private_workload_ci"}),
            source_ref="config/action-face-actions.json",
        ),
        SystemNode(
            name="GlacierEQ/llm-runner-teams",
            roles=frozenset({SystemRole.CONTROL_PLANE}),
            systems=frozenset({"github_actions.private_workload_ci"}),
            operations=ALL_OPERATIONS,
            private=True,
            source_ref="policy/no-private-actions.json",
        ),
    ]
    if include_receipt:
        nodes.append(
            SystemNode(
                name="GlacierEQ/llm-runner-teams/results",
                roles=frozenset({SystemRole.RECEIPT_PLANE}),
                systems=frozenset({"*"}),
                operations=ALL_OPERATIONS,
                private=True,
                source_ref="results/<job_id>.json",
            )
        )
    return ArchitectureSnapshot(
        snapshot_id="AKOS-TOPOLOGY-2026-07-21",
        source_refs=(
            "GlacierEQ/AKOS:AKOS_MANIFEST.yaml",
            "GlacierEQ/public-actions-runner-host:README.md",
            "GlacierEQ/llm-runner-teams:README.md",
        ),
        nodes=tuple(nodes),
        verified=verified,
    )


class SystemFirstTopologyTests(unittest.TestCase):
    def setUp(self):
        self.orchestrator = SystemFirstOrchestrator()

    def test_unverified_or_missing_topology_requires_discovery(self):
        route = self.orchestrator.resolve(work(), None)
        self.assertEqual(route.state, RouteState.DISCOVER)
        self.assertEqual(route.reason, "authoritative_topology_required")

        route = self.orchestrator.resolve(
            work(),
            canonical_snapshot(verified=False),
        )
        self.assertEqual(route.state, RouteState.DISCOVER)

    def test_existing_public_execution_route_is_resolved(self):
        route = self.orchestrator.resolve(work(), canonical_snapshot())
        self.assertEqual(route.state, RouteState.READY)
        self.assertEqual(
            route.execution_node,
            "GlacierEQ/public-actions-runner-host",
        )
        self.assertEqual(route.control_node, "GlacierEQ/llm-runner-teams")
        self.assertEqual(
            route.receipt_node,
            "GlacierEQ/llm-runner-teams/results",
        )
        self.assertNotIn("GlacierEQ/AKOS", [route.execution_node])

    def test_private_workflow_is_rejected_when_public_plane_exists(self):
        decision = self.orchestrator.evaluate_proposal(
            work(),
            canonical_snapshot(),
            ProposalKind.PRIVATE_WORKFLOW,
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(
            decision.reason,
            "private_workflow_duplicates_existing_execution_plane",
        )
        self.assertIn("public-actions-runner-host", decision.required_action)

    def test_new_runner_is_rejected_when_existing_plane_can_execute(self):
        decision = self.orchestrator.evaluate_proposal(
            work(),
            canonical_snapshot(),
            ProposalKind.NEW_RUNNER,
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(
            decision.reason,
            "existing_architecture_must_be_reused",
        )

    def test_unregistered_route_extends_catalog_not_infrastructure(self):
        target = work("document_packaging.private_workload")
        snapshot = canonical_snapshot(
            execution_systems=frozenset({"github_actions.private_workload_ci"})
        )
        route = self.orchestrator.resolve(target, snapshot)
        self.assertEqual(route.state, RouteState.EXTEND_EXISTING)
        self.assertIn("catalog action", route.next_action)
        self.assertIn("do not create", route.next_action)

        catalog = self.orchestrator.evaluate_proposal(
            target,
            snapshot,
            ProposalKind.CATALOG_ACTION,
        )
        self.assertTrue(catalog.allowed)

        runner = self.orchestrator.evaluate_proposal(
            target,
            snapshot,
            ProposalKind.NEW_RUNNER,
        )
        self.assertFalse(runner.allowed)

    def test_execution_without_receipt_plane_is_blocked(self):
        route = self.orchestrator.resolve(
            work(),
            canonical_snapshot(include_receipt=False),
        )
        self.assertEqual(route.state, RouteState.BLOCKED)
        self.assertEqual(route.reason, "receipt_plane_missing")

    def test_duplicate_architecture_nodes_are_rejected(self):
        snapshot = canonical_snapshot()
        duplicate = ArchitectureSnapshot(
            snapshot_id=snapshot.snapshot_id,
            source_refs=snapshot.source_refs,
            nodes=snapshot.nodes + (snapshot.nodes[0],),
            verified=True,
        )
        route = self.orchestrator.resolve(work(), duplicate)
        self.assertEqual(route.state, RouteState.BLOCKED)
        self.assertEqual(route.reason, "invalid_architecture_snapshot")


if __name__ == "__main__":
    unittest.main()
