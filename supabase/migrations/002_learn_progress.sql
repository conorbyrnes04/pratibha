-- Pratibha learn-path progress (run in Supabase SQL editor once).
-- Mirrors journal_notes: per-user JSON blob for gate completion + timestamps.

create table if not exists public.learn_progress (
  user_id uuid primary key references auth.users (id) on delete cascade,
  progress jsonb not null default '{}'::jsonb,
  completed_at jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.learn_progress enable row level security;

drop policy if exists "learn_progress_select_own" on public.learn_progress;
create policy "learn_progress_select_own"
  on public.learn_progress for select
  using (auth.uid() = user_id);

drop policy if exists "learn_progress_insert_own" on public.learn_progress;
create policy "learn_progress_insert_own"
  on public.learn_progress for insert
  with check (auth.uid() = user_id);

drop policy if exists "learn_progress_update_own" on public.learn_progress;
create policy "learn_progress_update_own"
  on public.learn_progress for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists "learn_progress_delete_own" on public.learn_progress;
create policy "learn_progress_delete_own"
  on public.learn_progress for delete
  using (auth.uid() = user_id);
