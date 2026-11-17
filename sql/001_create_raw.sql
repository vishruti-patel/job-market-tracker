create table if not exists raw_job_postings (
    load_date DATE not null,
    source text not null,
    company text not null,
    job_id text not null,
    internal_job_id text,
    title text,
    location_name text,
    updated_at timestamptz,
    raw_json jsonb not null,
    ingested_at timestamptz not null default now(),
    PRIMARY KEY (load_date, source, company, job_id)
)