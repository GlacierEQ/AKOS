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

export interface AkosObject {
  objectId: string;
  pillar: `P${number}`;
  lifecycleState: `L${number}`;
  objectType: string;
  title: string;
  content: string;
  sourcePointer: string;
  verificationStatus: VerificationStatus;
  actors: string[];
  tags: string[];
  contentHash: string;
  idempotencyKey: string;
  contradictionLinks: string[];
  disposition: Disposition;
  quarantineReason?: string;
}

export interface PipelineInput {
  title: string;
  content: string;
  sourcePointer: string;
  actors?: string[];
  tags?: string[];
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
