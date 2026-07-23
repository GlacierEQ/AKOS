-- CASEBRAIN SECURITY REPAIR — REVIEW ONLY
-- Target project: supabase-backend-ops (dyhprklicgewmrimecey)
-- Generated: 2026-07-15
-- IMPORTANT: This file has NOT been applied.
-- Apply only after review against live function definitions and explicit approval.

begin;

-- 1. Pin mutable search_path on known helper.
alter function public.set_updated_at() set search_path = pg_catalog, public;

-- 2. Remove broad execution from exposed SECURITY DEFINER RPCs.
revoke execute on function public.claim_next_run_request() from public, anon, authenticated;
revoke execute on function public.cleanup_old_jobs(integer) from public, anon, authenticated;
revoke execute on function public.create_conversation(text, uuid[]) from public, anon, authenticated;
revoke execute on function public.enqueue_run_request(text, jsonb) from public, anon, authenticated;
revoke execute on function public.finish_run_request(uuid, boolean, jsonb) from public, anon, authenticated;
revoke execute on function public.track_operator_event(text, integer, jsonb, double precision) from public, anon, authenticated;
revoke execute on function public.update_conversation_last_message() from public, anon, authenticated;
revoke execute on function public.user_has_file_access(public.files) from public, anon, authenticated;
revoke execute on function public.user_has_file_access(uuid, uuid) from public, anon, authenticated;

-- 3. Restore least-privilege execution only to service_role where orchestration requires it.
grant execute on function public.claim_next_run_request() to service_role;
grant execute on function public.cleanup_old_jobs(integer) to service_role;
grant execute on function public.enqueue_run_request(text, jsonb) to service_role;
grant execute on function public.finish_run_request(uuid, boolean, jsonb) to service_role;
grant execute on function public.track_operator_event(text, integer, jsonb, double precision) to service_role;

-- Conversation/file-access functions remain intentionally ungranted pending policy review.

commit;

-- OUT-OF-BAND PLATFORM CONTROLS (not expressible safely in this migration):
-- A. Reduce email OTP expiry to <= 3600 seconds in Auth settings.
-- B. Upgrade Supabase Postgres to the latest patched release through the platform upgrade flow.
-- C. Re-run security and performance advisors after application.
-- D. Verify no application path depends on anon/authenticated access to revoked RPCs.
