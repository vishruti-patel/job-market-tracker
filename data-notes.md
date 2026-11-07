# Data notes: Greenhouse Job Board API

## Endpoint
- List jobs: GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs
- Auth: none needed for reading
- ?content=true adds the job description (HTML)
- Returns only currently open jobs; closed jobs disappear from the response

## Grain
- One record = one open job posting on one company's board, as seen at the time of the call

## Natural key
- company (board token) + id (job post ID)
- Not internal_job_id: one internal job can have several posts (to verify in Phase 2)

## Fields I'll keep as columns in raw_job_postings
| Field in API | Example value | Why I keep it |
| --- | --- | --- |
| id | (from response) | Natural key |
| internal_job_id | 6523784002 | Groups several posts of the same role |
| title | Senior Data Engineer | Most-queried field |
| location.name | Remote, US | Nested object; extracted for dim_location |
| updated_at | (from response) | Detect changes between days |
| absolute_url | (from response) | Link back to the posting |
| everything else | full record | Kept in raw_json |

## Observations
- Jobs returned: gitlab ~280, databricks ~900
- Time without / with content=true: 91 ms / 1.20 s (~13x slower)
- Size without / with content=true: __ / __
- Wrong board token: status 400 -> treat any non-200 as failure, log, continue
- location is nested; descriptions are HTML; custom fields (e.g. application deadline) vary by company

## Decisions
- Use content=true: descriptions are needed for skills, and the source deletes closed jobs, so raw must capture them now

## Open questions
- Is id unique within a board? (test in Phase 2)
- Does internal_job_id repeat? (test in Phase 2)