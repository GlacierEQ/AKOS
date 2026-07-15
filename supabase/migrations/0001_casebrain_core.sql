begin;

create extension if not exists pgcrypto;

create table if not exists public.casebrain_objects (
  id uuid primary key default gen_random_uuid(),
  casebrain_id text not null unique,
  object_type text not null check (object_type in (
    'case','actor','event','evidence','claim','contradiction','authority','filing',
    'task','relationship','connector_object','sync_run','sync_receipt','verification_event'
  )),
  case_id text not null,
  title text not null,
  summary text,
  verification_status text not null default 'unverified' check (verification_status in (
    'unverified','machine_extracted','human_reviewed','verified','disputed','superseded'
  )),
  confidence numeric check (confidence is null or (confidence >= 0 and confidence <= 1)),
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists casebrain_objects_case_id_idx on public.casebrain_objects(case_id);
create index if not exists casebrain_objects_type_idx on public.casebrain_objects(object_type);
create index if not exists casebrain_objects_payload_gin_idx on public.casebrain_objects using gin(payload);

create table if not exists public.source_objects (
  id uuid primary key default gen_random_uuid(),
  casebrain_id text not null references public.casebrain_objects(casebrain_id) on delete restrict,
  source_system text not null,
  source_uri text not null,
  source_object_id text,
  sha256 text check (sha256 is null or sha256 ~ '^[a-f0-9]{64}$'),
  mime_type text,
  page_start integer check (page_start is null or page_start > 0),
  page_end integer check (page_end is null or page_end > 0),
  line_start integer check (line_start is null or line_start > 0),
  line_end integer check (line_end is null or line_end > 0),
  time_start_ms bigint check (time_start_ms is null or time_start_ms >= 0),
  time_end_ms bigint check (time_end_ms is null or time_end_ms >= 0),
  extraction_method text,
  is_original boolean not null default false,
  created_at timestamptz not null default now(),
  unique(source_system, source_uri, coalesce(sha256, ''))
);

create table if not exists public.object_relationships (
  id uuid primary key default gen_random_uuid(),
  source_casebrain_id text not null references public.casebrain_objects(casebrain_id) on delete restrict,
  predicate text not null,
  target_casebrain_id text not null references public.casebrain_objects(casebrain_id) on delete restrict,
  confidence numeric check (confidence is null or (confidence >= 0 and confidence <= 1)),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique(source_casebrain_id, predicate, target_casebrain_id)
);

create table if not exists public.connector_crosswalk (
  id uuid primary key default gen_random_uuid(),
  casebrain_id text not null references public.casebrain_objects(casebrain_id) on delete restrict,
  connector text not null,
  remote_object_id text not null,
  remote_parent_id text,
  remote_url text,
  projection_version integer not null default 1,
  payload_hash text not null,
  last_synced_at timestamptz not null default now(),
  unique(connector, remote_object_id),
  unique(casebrain_id, connector, coalesce(remote_parent_id, ''))
);

create table if not exists public.sync_receipts (
  id uuid primary key default gen_random_uuid(),
  receipt_id text not null unique,
  idempotency_key text not null unique,
  operation_type text not null,
  casebrain_id text references public.casebrain_objects(casebrain_id) on delete restrict,
  connector text not null,
  request_hash text not null,
  response_hash text,
  status text not null check (status in ('planned','started','succeeded','partially_succeeded','failed','reverted')),
  remote_object_id text,
  remote_url text,
  prior_state jsonb,
  result jsonb not null default '{}'::jsonb,
  error jsonb,
  started_at timestamptz not null default now(),
  completed_at timestamptz
);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger casebrain_objects_set_updated_at
before update on public.casebrain_objects
for each row execute function public.set_updated_at();

alter table public.casebrain_objects enable row level security;
alter table public.source_objects enable row level security;
alter table public.object_relationships enable row level security;
alter table public.connector_crosswalk enable row level security;
alter table public.sync_receipts enable row level security;

comment on table public.casebrain_objects is 'Canonical CASEBRAIN operational objects.';
comment on table public.source_objects is 'Immutable source pointers and provenance anchors; original bytes remain in approved storage.';
comment on table public.sync_receipts is 'Append-only connector operation receipts and idempotency ledger.';

commit;