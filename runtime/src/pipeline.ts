import { createHash } from "node:crypto";
import type {
  AkosObject,
  ArtifactTwin,
  Claim,
  ContradictionEdge,
  PipelineInput,
  VerificationStatus,
} from "./contracts.js";

const SECRET_PATTERNS: RegExp[] = [
  /gh[pousr]_[A-Za-z0-9_]{20,}/,
  /sk-[A-Za-z0-9_-]{20,}/,
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,
  /(?:api[_-]?key|token|password)\s*[:=]\s*[^\s]+/i,
];

export function sha256(value: string): string {
  return createHash("sha256").update(value, "utf8").digest("hex");
}

export function normalizeText(value: string): string {
  return value
    .normalize("NFKC")
    .replace(/\r\n/g, "\n")
    .replace(/[ \t]+/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

export function containsSecret(value: string): boolean {
  return SECRET_PATTERNS.some((pattern) => pattern.test(value));
}

function inferVerificationStatus(input: PipelineInput): VerificationStatus {
  const source = input.sourcePointer.toLowerCase();
  if (source.startsWith("github:") || source.startsWith("court:") || source.startsWith("sha256:")) {
    return "verified_record";
  }
  return "unresolved";
}

export function processInput(input: PipelineInput): AkosObject {
  const normalized = normalizeText(input.content);
  const contentHash = sha256(normalized);
  const objectId = `AKOS-${contentHash.slice(0, 16)}`;
  const quarantined = containsSecret(normalized);
  const verificationStatus = inferVerificationStatus(input);

  return {
    objectId,
    pillar: quarantined ? "P9" : "P4",
    lifecycleState: quarantined ? "L1" : verificationStatus === "verified_record" ? "L3" : "L2",
    objectType: "knowledge_object",
    title: normalizeText(input.title),
    content: quarantined ? "[REDACTED: secret-bearing content quarantined]" : normalized,
    sourcePointer: input.sourcePointer,
    verificationStatus,
    actors: [...new Set(input.actors ?? [])].sort(),
    tags: [...new Set(input.tags ?? [])].sort(),
    contentHash,
    idempotencyKey: sha256(`${input.sourcePointer}:${contentHash}`),
    contradictionLinks: [],
    disposition: quarantined
      ? "QUARANTINE"
      : verificationStatus === "verified_record"
        ? "PROMOTE"
        : "MANUAL_REVIEW",
    ...(quarantined ? { quarantineReason: "secret_pattern_detected" } : {}),
  };
}

export function buildEvidenceManifest(objects: AkosObject[]): string {
  const leaves = objects
    .map((object) => `${object.objectId}:${object.contentHash}`)
    .sort();
  return sha256(leaves.join("\n"));
}

export function buildContradictionGraph(claims: Claim[]): ContradictionEdge[] {
  const edges: ContradictionEdge[] = [];
  for (let leftIndex = 0; leftIndex < claims.length; leftIndex += 1) {
    const left = claims[leftIndex];
    if (!left) continue;
    for (let rightIndex = leftIndex + 1; rightIndex < claims.length; rightIndex += 1) {
      const right = claims[rightIndex];
      if (!right) continue;
      if (
        left.subject === right.subject &&
        left.predicate === right.predicate &&
        left.value !== right.value
      ) {
        edges.push({
          leftClaimId: left.claimId,
          rightClaimId: right.claimId,
          reason: `Conflicting values for ${left.subject}.${left.predicate}`,
        });
      }
    }
  }
  return edges;
}

export function createArtifactTwin(object: AkosObject): ArtifactTwin {
  if (object.disposition === "QUARANTINE") {
    throw new Error("Quarantined objects cannot produce artifacts");
  }

  return {
    markdown: [
      `# ${object.title}`,
      "",
      `- Object ID: \`${object.objectId}\``,
      `- Verification: \`${object.verificationStatus}\``,
      `- Source: \`${object.sourcePointer}\``,
      `- SHA-256: \`${object.contentHash}\``,
      "",
      object.content,
    ].join("\n"),
    json: object,
  };
}
