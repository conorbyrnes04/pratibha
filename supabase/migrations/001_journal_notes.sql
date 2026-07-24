-- Pratibha journal notes (run in Supabase SQL editor once).
-- Auth: enable Email + Google in Authentication → Providers first.

create table if not exists public.journal_notes (
  id text primary key,
  user_id uuid not null references auth.users (id) on delete cascade,
  passage_id text not null,
  passage_title text not null default '',
  body text not null default '',
  tags text[] not null default '{}',
  prompt text,
  kind text,
  question text,
  chat_mode text,
  verse_id text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists journal_notes_user_updated_idx
  on public.journal_notes (user_id, updated_at desc);

alter table public.journal_notes enable row level security;

drop policy if exists "journal_select_own" on public.journal_notes;
create policy "journal_select_own"
  on public.journal_notes for select
  using (auth.uid() = user_id);

drop policy if exists "journal_insert_own" on public.journal_notes;
create policy "journal_insert_own"
  on public.journal_notes for insert
  with check (auth.uid() = user_id);

drop policy if exists "journal_update_own" on public.journal_notes;
create policy "journal_update_own"
  on public.journal_notes for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists "journal_delete_own" on public.journal_notes;
create policy "journal_delete_own"
  on public.journal_notes for delete
  using (auth.uid() = user_id);
