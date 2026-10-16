-- ============================================================================
-- Flutter Pro Max Telemetry & Knowledge Gap Feedback Schema
-- Execute in Supabase SQL Editor: https://supabase.com/dashboard/project/_/sql
-- ============================================================================

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. Table: Knowledge Gaps (Tra cứu thiếu hoặc tìm kiếm gượng ép)
create table if not exists public.knowledge_gaps (
    id uuid primary key default uuid_generate_v4(),
    query text not null,
    domain text not null,
    gap_type text not null, -- 'empty_result' | 'weak_match' | 'explicit_report' | 'stack_incompatible'
    result_count integer default 0,
    max_score numeric(6, 4) default 0.0,
    token_coverage numeric(4, 2) default 0.0,
    stack text,
    notes text,
    ai_assistant text,
    client_os text,
    skill_version text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Indexes for lightning-fast aggregation & search
create index if not exists idx_knowledge_gaps_query on public.knowledge_gaps (lower(query));
create index if not exists idx_knowledge_gaps_domain on public.knowledge_gaps (domain);
create index if not exists idx_knowledge_gaps_created_at on public.knowledge_gaps (created_at desc);

-- 2. Table: Criteria Gaps (Tiêu chí chấm điểm UI/UX audit thiếu)
create table if not exists public.criteria_gaps (
    id uuid primary key default uuid_generate_v4(),
    missing_dimensions text[] not null,
    platforms text[] not null,
    gap_type text not null, -- 'unrecognized_dimension' | 'explicit_report'
    reason text,
    notes text,
    ai_assistant text,
    client_os text,
    skill_version text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

create index if not exists idx_criteria_gaps_created_at on public.criteria_gaps (created_at desc);

-- 3. Analytics Views for Quick Insights
-- View: Top 20 từ khóa tra cứu bị thiếu nhiều nhất
create or replace view public.v_top_knowledge_gaps as
select 
    lower(query) as query_text,
    domain,
    count(*) as total_misses,
    max(created_at) as last_seen,
    array_agg(distinct ai_assistant) as reported_by_assistants
from public.knowledge_gaps
group by lower(query), domain
order by total_misses desc
limit 50;

-- View: Tiêu chí UI/UX thiếu nhiều nhất
create or replace view public.v_top_criteria_gaps as
select 
    unnest(missing_dimensions) as missing_criterion,
    count(*) as total_occurrences,
    max(created_at) as last_seen
from public.criteria_gaps
group by missing_criterion
order by total_occurrences desc;

-- 4. Row Level Security (RLS)
-- Allow public / anon users to INSERT events (telemetry reporting)
alter table public.knowledge_gaps enable row level security;
alter table public.criteria_gaps enable row level security;

create policy "Allow anonymous telemetry ingestion"
on public.knowledge_gaps for insert
with check (true);

create policy "Allow anonymous criteria gap ingestion"
on public.criteria_gaps for insert
with check (true);

-- Only authenticated users (dashboard owner) can SELECT / READ
create policy "Allow owner to view knowledge gaps"
on public.knowledge_gaps for select
using (auth.role() = 'authenticated');

create policy "Allow owner to view criteria gaps"
on public.criteria_gaps for select
using (auth.role() = 'authenticated');
