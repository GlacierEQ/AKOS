import assert from "node:assert/strict";
import type { AddressInfo } from "node:net";
import test from "node:test";
import { createAkosServer } from "../src/index.js";
import {
  buildContradictionGraph,
  buildEvidenceManifest,
  createArtifactTwin,
  normalizeText,
  processInput,
} from "../src/pipeline.js";

const COMMIT_SHA = "a".repeat(40);
const RECORD_HASH = "b".repeat(64);

test("normalization and object identity are deterministic", () => {
  assert.equal(normalizeText("  Alpha\r\n\r\n\r\nBeta  "), "Alpha\n\nBeta");

  const first = processInput({
    title: " Test Object ",
    content: "Alpha   Beta",
    sourcePointer: "user:casey",
  });
  const second = processInput({
    title: "Test Object",
    content: "Alpha Beta",
    sourcePointer: "user:casey",
  });

  assert.equal(first.objectId, second.objectId);
  assert.equal(first.idempotencyKey, second.idempotencyKey);
});

test("a mutable GitHub-looking pointer cannot self-promote", () => {
  const object = processInput({
    title: "Mutable source",
    content: "Unverified content",
    sourcePointer: "github:GlacierEQ/AKOS:main/runtime/src/index.ts",
    sourceClass: "authenticated_repository",
    verificationStatus: "verified_record",
  });

  assert.equal(object.verificationStatus, "unresolved");
  assert.equal(object.disposition, "MANUAL_REVIEW");
  assert.ok(object.gatesFailed.length === 0);
});

test("an immutable authenticated repository pointer may promote", () => {
  const object = processInput({
    title: "Committed source",
    content: "Repository-backed content",
    sourcePointer: `github:GlacierEQ/AKOS@${COMMIT_SHA}:runtime/src/index.ts`,
    sourceClass: "authenticated_repository",
    verificationStatus: "verified_record",
    objectType: "system_architecture",
  });

  assert.equal(object.verificationStatus, "verified_record");
  assert.equal(object.disposition, "PROMOTE");
  assert.equal(object.pillar, "P4");
  assert.equal(object.lifecycleState, "L3");
});

test("primary records require an immutable evidence hash", () => {
  const object = processInput({
    title: "Court record",
    content: "Authenticated docket fact",
    sourcePointer: `court:1FDV-23-0001009/Dkt.215#sha256:${RECORD_HASH}`,
    sourceClass: "primary_record",
    verificationStatus: "verified_record",
    objectType: "evidence_record",
    caseId: "1FDV-23-0001009",
  });

  assert.equal(object.verificationStatus, "verified_record");
  assert.equal(object.pillar, "P1");
  assert.equal(object.disposition, "PROMOTE");
});

test("secret-bearing material is quarantined without reproducing the secret", () => {
  const rawSecret = `ghp_${"x".repeat(32)}`;
  const object = processInput({
    title: "Credential fragment",
    content: `token=${rawSecret}`,
    sourcePointer: "chat:legacy-import",
  });

  assert.equal(object.disposition, "QUARANTINE");
  assert.equal(object.pillar, "P9");
  assert.equal(object.lifecycleState, "L1");
  assert.ok(!JSON.stringify(object).includes(rawSecret));
  assert.ok(object.secretFingerprints?.some((value) => value.startsWith("github_token:")));
  assert.throws(() => createArtifactTwin(object), /Quarantined objects/);
});

test("court-facing artifacts reject unresolved sources", () => {
  const object = processInput({
    title: "Unresolved declaration",
    content: "User-provided narrative",
    sourcePointer: "user:casey",
    sourceClass: "user_submission",
    verificationStatus: "user_assertion",
    courtFacing: true,
  });

  assert.equal(object.disposition, "MANUAL_REVIEW");
  assert.ok(object.gatesFailed.includes("G6_legal_safe"));
  assert.throws(
    () => createArtifactTwin(object, { courtFacing: true }),
    /verified_record/,
  );
});

test("evidence manifest is stable across order and duplicate inputs", () => {
  const first = processInput({ title: "A", content: "One", sourcePointer: "user:a" });
  const second = processInput({ title: "B", content: "Two", sourcePointer: "user:b" });

  assert.equal(
    buildEvidenceManifest([first, second, first]),
    buildEvidenceManifest([second, first]),
  );
});

test("contradiction graph emits explicit conflict edges", () => {
  const edges = buildContradictionGraph([
    {
      claimId: "claim-1",
      subject: "Dkt. 193",
      predicate: "custody-holder",
      value: "Plaintiff",
      sourceObjectId: "object-1",
    },
    {
      claimId: "claim-2",
      subject: "dkt. 193",
      predicate: "custody-holder",
      value: "Defendant",
      sourceObjectId: "object-2",
    },
  ]);

  assert.deepEqual(edges, [
    {
      leftClaimId: "claim-1",
      rightClaimId: "claim-2",
      reason: "Conflicting values for Dkt. 193.custody-holder",
    },
  ]);
});

test("HTTP surface exposes health and executes the guarded pipeline", async () => {
  const server = createAkosServer();
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));

  try {
    const address = server.address() as AddressInfo;
    const baseUrl = `http://127.0.0.1:${address.port}`;

    const health = await fetch(`${baseUrl}/health`);
    assert.equal(health.status, 200);
    const healthPayload = await health.json() as { status: string; pistons: number };
    assert.equal(healthPayload.status, "ok");
    assert.ok(healthPayload.pistons >= 7);

    const execution = await fetch(`${baseUrl}/execute`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        title: "Committed source",
        content: "Repository-backed content",
        sourcePointer: `github:GlacierEQ/AKOS@${COMMIT_SHA}:runtime/src/index.ts`,
        sourceClass: "authenticated_repository",
        verificationStatus: "verified_record",
      }),
    });
    assert.equal(execution.status, 200);
    const executionPayload = await execution.json() as {
      object: { disposition: string };
      manifestRoot: string;
    };
    assert.equal(executionPayload.object.disposition, "PROMOTE");
    assert.match(executionPayload.manifestRoot, /^[a-f0-9]{64}$/);
  } finally {
    await new Promise<void>((resolve, reject) => {
      server.close((error) => error ? reject(error) : resolve());
    });
  }
});
