create extension if not exists "pgcrypto";

create table if not exists users (
  user_id uuid primary key references auth.users(id) on delete cascade,
  username text unique not null,
  full_name text not null,
  email text unique not null,
  created_at timestamptz default now()
);
create table organizations (organization_id uuid primary key default gen_random_uuid(), name text not null, type text not null, created_at timestamptz default now(), created_by_user_id uuid references users(user_id));
create table organization_memberships (membership_id uuid primary key default gen_random_uuid(), organization_id uuid references organizations(organization_id) on delete cascade, user_id uuid references users(user_id), role text not null, status text not null, joined_at timestamptz default now(), unique(organization_id,user_id));
create table teams (team_id uuid primary key default gen_random_uuid(), organization_id uuid references organizations(organization_id) on delete cascade, name text not null, description text default '', created_at timestamptz default now(), created_by_user_id uuid references users(user_id));
create table team_members (team_member_id uuid primary key default gen_random_uuid(), team_id uuid references teams(team_id) on delete cascade, user_id uuid references users(user_id), role text not null, status text not null, joined_at timestamptz default now(), unique(team_id,user_id));
create table subgroups (subgroup_id uuid primary key default gen_random_uuid(), team_id uuid references teams(team_id) on delete cascade, name text not null, created_at timestamptz default now(), created_by_user_id uuid references users(user_id));
create table subgroup_members (subgroup_member_id uuid primary key default gen_random_uuid(), subgroup_id uuid references subgroups(subgroup_id) on delete cascade, user_id uuid references users(user_id), joined_at timestamptz default now(), unique(subgroup_id,user_id));
create table routines (routine_id uuid primary key default gen_random_uuid(), team_id uuid references teams(team_id) on delete cascade, title text not null, created_at timestamptz default now(), created_by_user_id uuid references users(user_id));
create table videos (video_id uuid primary key default gen_random_uuid(), routine_id uuid references routines(routine_id) on delete cascade, uploaded_by_user_id uuid references users(user_id), file_url text not null, storage_path text not null, version_number int not null, recorded_at timestamptz null, uploaded_at timestamptz default now(), duration_seconds numeric);
create table comments (comment_id uuid primary key default gen_random_uuid(), video_id uuid references videos(video_id) on delete cascade, author_user_id uuid references users(user_id), body text not null, video_timestamp_seconds numeric not null, target_type text check (target_type in ('individual','subgroup','team')) not null, created_at timestamptz default now(), updated_at timestamptz default now(), status text check(status in ('open','resolved')) default 'open', resolved_by_user_id uuid references users(user_id), resolved_at timestamptz null);
create table comment_targets (comment_target_id uuid primary key default gen_random_uuid(), comment_id uuid references comments(comment_id) on delete cascade, user_id uuid references users(user_id), subgroup_id uuid references subgroups(subgroup_id), team_id uuid references teams(team_id));
create table comment_recipients (comment_recipient_id uuid primary key default gen_random_uuid(), comment_id uuid references comments(comment_id) on delete cascade, user_id uuid references users(user_id), seen_at timestamptz null, acknowledged_at timestamptz null, status text default 'open', unique(comment_id, user_id));

alter table users enable row level security;
create policy "users_select_self" on users for select using (auth.uid() = user_id);
