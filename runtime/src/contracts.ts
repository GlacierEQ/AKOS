export type VerificationStatus =
  | "verified_record"
  | "user_assertion"
  | "inference"
  | "draft_strategy"
  | "unresolved";

export type Disposition =
  | "PROMOTE"
  | "DEDUPLICATE"
  | "QUARANTINE"
  | "MANUAL_REVIEW"
  | "READ_ONLY_ALIAS";

export type Pillar =
  | "P0"
  | "P1"
  | "P2"
  | "P3"
  | "P4"
  | "P5"
  | "P6"
  | "P7"
  | "P8"
  | "P9";

export type LifecycleState =
  | "L0"
  | "L1"
  | "L2"
  | "L3"
  | "L4"
  | "L5"
  | "L6"
  | "L7"
  | "L8"
  | "L9";

export type SourceClass =
  | "primary_record"
  | "authenticated_repository"
  | "derivative"
  | "user_submission"
  | "unknown";

export interface AkosObject {
  objectId: string;
  pillar: Pillar;
  lifecycleState: LifecycleState;
  objectType: string;
  title: string;
  content: string;
  sourcePointer: string;
  sourceClass: SourceClass;
  verificationStatus: VerificationStatus;
  actors: string[];
  tags: string[];
  contentHash: string;
  idempotencyKey: string;
  contradictionLinks: string[];
  disposition: Disposition;
  gatesPassed: string[];
  gatesFailed: string[];
  caseId?: string;
  eventDate?: string;
  quarantineReason?: string;
  secretFingerprints?: string[];
}

export interface PipelineInput {
  title: string;
  content: string;
  sourcePointer: string;
  sourceClass?: SourceClass;
  verificationStatus?: VerificationStatus;
  objectType?: string;
  caseId?: string;
  eventDate?: string;
  pillarHint?: Pillar;
  actors?: string[];
  tags?: string[];
  courtFacing?: boolean;
}

export interface Claim {
  claimId: string;
  subject: string;
  predicate: string;
  value: string;
  sourceObjectId: string;
}

export interface ContradictionEdge {
  leftClaimId: string;
  rightClaimId: string;
  reason: string;
}

export interface ArtifactTwin {
  markdown: string;
  json: AkosObject;
}

export interface ArtifactOptions {
  courtFacing?: boolean;
}
