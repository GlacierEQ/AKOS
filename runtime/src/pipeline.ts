import { createHash } from "node:crypto";
import type {
  AkosObject,
  ArtifactOptions,
  ArtifactTwin,
  Claim,
  ContradictionEdge,
  Pillar,
  PipelineInput,
  SourceClass,
  VerificationStatus,
} from "./contracts.js";

const SECRET_PATTERNS: ReadonlyArray<{ name: string; pattern: RegExp }> = [
  { name: "github_token", pattern: /gh[pousr]_[A-Za-z0-9_]{20,}/ },
  { name: "openai_key", pattern: /sk-[A-Za-z0-9_-]{20,}/ },
  { name: "private_key", pattern: /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/ },
  { name: "named_credential", pattern: /(?:api[_-]?key|token|password)\s*[:=]\s*[^\s]+/i },
];

const VERIFIED_SOURCE_CLASSES = new Set<SourceClass>([
  "primary_record",
  "authenticated_repository",
]);

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

function normalizeList(values: string[] | undefined): string[] {
  return [...new Set((values ?? []).map(normalizeText).filter(Boolean))].sort();
}

export function scanSecretFingerprints(value: string): string[] {
  const fingerprints = SECRET_PATTERNS.flatMap(({ name, pattern }) => {
    const match = value.match(pattern);
    return match ? [`${name}:${sha256(match[0]).slice(0, 16)}`] : [];
  });
  return [...new Set(fingerprints)].sort();
}

export function containsSecret(value: string): boolean {
  return scanSecretFingerprints(value).length > 0;
}

function hasImmutableSourcePointer(sourceClass: SourceClass, sourcePointer: string): boolean {
  if (sourceClass === "authenticated_repository") {
    return /^github:[^@\s]+@[a-f0-9]{40}(?::[^\s]+)?$/i.test(sourcePointer);
  }
  if (sourceClass === "primary_record") {
    return /^(?:court|evidence):.+#sha256:[a-f0-9]{64}$/i.test(sourcePointer)
      || /^sha256:[a-f0-9]{64}$/i.test(sourcePointer);
  }
  return false;
}

function inferVerificationStatus(input: PipelineInput, sourceClass: SourceClass): VerificationStatus {
  const requested = input.verificationStatus ?? "unresolved";
  if (requested !== "verified_record") return requested;

  return VERIFIED_SOURCE_CLASSES.has(sourceClass)
    && hasImmutableSourcePointer(sourceClass, input.sourcePointer.trim())
    ? "verified_record"
    : "unresolved";
}

function routePillar(input: PipelineInput, quarantined: boolean): Pillar {
  if (quarantined) return "P9";
  if (input.caseId) return "P1";

  const objectType = (input.objectType ?? "knowledge_object").toLowerCase();
  if (objectType.includes("evidence") || objectType.includes("communication")) return "P3";
  if (objectType.includes("architecture") || objectType.includes("system")) return "P4";
  if (objectType.includes("task") || objectType.includes("queue")) return "P8";
  return input.pillarHint ?? "P7";
}

function requireNonEmptyString(value: unknown, field: string): string {
  if (typeof value !== "string" || normalizeText(value).length === 0) {
    throw new TypeError(`${field} must be a non-empty string`);
  }
  return value;
}

function optionalString(value: unknown, field: string): string | undefined {
  if (value === undefined) return undefined;
  if (typeof value !== "string") throw new TypeError(`${field} must be a string`);
  const normalized = normalizeText(value);
  return normalized || undefined;
}

function optionalStringArray(value: unknown, field: string): string[] | undefined {
  if (value === undefined) return undefined;
  if (!Array.isArray(value) || value.some((item) => typeof item !== "string")) {
    throw new TypeError(`${field} must be an array of strings`);
  }
  return value as string[];
}

export function parsePipelineInput(value: unknown): PipelineInput {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new TypeError("request body must be a JSON object");
  }

  const record = value as Record<string, unknown>;
  const sourceClass = optionalString(record.sourceClass, "sourceClass") as SourceClass | undefined;
  const verificationStatus = optionalString(
    record.verificationStatus,
    "verificationStatus",
  ) as VerificationStatus | undefined;
  const pillarHint = optionalString(record.pillarHint, "pillarHint") as Pillar | undefined;

  const allowedSourceClasses = new Set<SourceClass>([
    "primary_record",
    "authenticated_repository",
    "derivative",
    "user_submission",
    "unknown",
  ]);
  const allowedStatuses = new Set<VerificationStatus>([
    "verified_record",
    "user_assertion",
    "inference",
    "draft_strategy",
    "unresolved",
  ]);
  const allowedPillars = new Set<Pillar>([
    "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9",
  ]);

  if (sourceClass && !allowedSourceClasses.has(sourceClass)) {
    throw new TypeError("sourceClass is invalid");
  }
  if (verificationStatus && !allowedStatuses.has(verificationStatus)) {
    throw new TypeError("verificationStatus is invalid");
  }
  if (pillarHint && !allowedPillars.has(pillarHint)) {
    throw new TypeError("pillarHint is invalid");
  }
  if (record.courtFacing !== undefined && typeof record.courtFacing !== "boolean") {
    throw new TypeError("courtFacing must be a boolean");
  }

  const objectType = optionalString(record.objectType, "objectType");
  const caseId = optionalString(record.caseId, "caseId");
  const eventDate = optionalString(record.eventDate, "eventDate");
  const actors = optionalStringArray(record.actors, "actors");
  const tags = optionalStringArray(record.tags, "tags");

  return {
    title: requireNonEmptyString(record.title, "title"),
    content: requireNonEmptyString(record.content, "content"),
    sourcePointer: requireNonEmptyString(record.sourcePointer, "sourcePointer"),
    ...(sourceClass ? { sourceClass } : {}),
    ...(verificationStatus ? { verificationStatus } : {}),
    ...(objectType ? { objectType } : {}),
    ...(caseId ? { caseId } : {}),
    ...(eventDate ? { eventDate } : {}),
    ...(pillarHint ? { pillarHint } : {}),
    ...(actors ? { actors } : {}),
    ...(tags ? { tags } : {}),
    ...(typeof record.courtFacing === "boolean" ? { courtFacing: record.courtFacing } : {}),
  };
}

export function processInput(input: PipelineInput): AkosObject {
  const normalizedTitle = normalizeText(input.title);
  const normalizedContent = normalizeText(input.content);
  const normalizedSourcePointer = input.sourcePointer.trim();
  const sourceClass = input.sourceClass ?? "unknown";
  const secretFingerprints = scanSecretFingerprints(
    `${normalizedTitle}\n${normalizedContent}\n${normalizedSourcePointer}`,
  );
  const quarantined = secretFingerprints.length > 0;
  const verificationStatus = inferVerificationStatus(input, sourceClass);
  const contentHash = sha256(
    `${normalizedTitle}\n${normalizedContent}\n${normalizedSourcePointer}`,
  );
  const objectId = `AKOS-${contentHash.slice(0, 16)}`;
  const legalSafe = input.courtFacing !== true || verificationStatus === "verified_record";

  const gatesPassed = [
    ...(quarantined ? [] : ["G1_secret_safe"]),
    "G2_identity_safe",
    "G3_provenance_classified",
    "G4_verification_classified",
    ...(legalSafe ? ["G6_legal_safe"] : []),
    "G7_idempotency_safe",
  ];
  const gatesFailed = [
    ...(quarantined ? ["G1_secret_safe"] : []),
    ...(legalSafe ? [] : ["G6_legal_safe"]),
  ];

  return {
    objectId,
    pillar: routePillar(input, quarantined),
    lifecycleState: quarantined ? "L1" : verificationStatus === "verified_record" ? "L3" : "L2",
    objectType: input.objectType ?? "knowledge_object",
    title: quarantined ? "[REDACTED: secret-bearing object]" : normalizedTitle,
    content: quarantined ? "[REDACTED: secret-bearing content quarantined]" : normalizedContent,
    sourcePointer: quarantined
      ? `secret_ref:${secretFingerprints[0] ?? sha256(normalizedSourcePointer).slice(0, 16)}`
      : normalizedSourcePointer,
    sourceClass,
    verificationStatus,
    actors: normalizeList(input.actors),
    tags: normalizeList(input.tags),
    contentHash,
    idempotencyKey: sha256(`${sourceClass}:${normalizedSourcePointer}:${contentHash}`),
    contradictionLinks: [],
    disposition: quarantined
      ? "QUARANTINE"
      : verificationStatus === "verified_record" && legalSafe
        ? "PROMOTE"
        : "MANUAL_REVIEW",
    gatesPassed,
    gatesFailed,
    ...(input.caseId ? { caseId: normalizeText(input.caseId) } : {}),
    ...(input.eventDate ? { eventDate: normalizeText(input.eventDate) } : {}),
    ...(quarantined ? { quarantineReason: "secret_pattern_detected", secretFingerprints } : {}),
  };
}

export function buildEvidenceManifest(objects: AkosObject[]): string {
  const uniqueLeaves = new Set(
    objects.map((object) => `${object.objectId}:${object.contentHash}:${object.sourcePointer}`),
  );
  return sha256([...uniqueLeaves].sort().join("\n"));
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
        normalizeText(left.subject).toLowerCase() === normalizeText(right.subject).toLowerCase()
        && normalizeText(left.predicate).toLowerCase() === normalizeText(right.predicate).toLowerCase()
        && normalizeText(left.value) !== normalizeText(right.value)
      ) {
        edges.push({
          leftClaimId: left.claimId,
          rightClaimId: right.claimId,
          reason: `Conflicting values for ${normalizeText(left.subject)}.${normalizeText(left.predicate)}`,
        });
      }
    }
  }
  return edges.sort((left, right) =>
    `${left.leftClaimId}:${left.rightClaimId}`.localeCompare(`${right.leftClaimId}:${right.rightClaimId}`),
  );
}

export function createArtifactTwin(
  object: AkosObject,
  options: ArtifactOptions = {},
): ArtifactTwin {
  if (object.disposition === "QUARANTINE") {
    throw new Error("Quarantined objects cannot produce artifacts");
  }
  if (options.courtFacing === true && object.verificationStatus !== "verified_record") {
    throw new Error("Court-facing artifacts require verified_record source status");
  }

  return {
    markdown: [
      `# ${object.title}`,
      "",
      `- Object ID: \`${object.objectId}\``,
      `- Verification: \`${object.verificationStatus}\``,
      `- Source class: \`${object.sourceClass}\``,
      `- Source: \`${object.sourcePointer}\``,
      `- SHA-256: \`${object.contentHash}\``,
      "",
      object.content,
    ].join("\n"),
    json: object,
  };
}
