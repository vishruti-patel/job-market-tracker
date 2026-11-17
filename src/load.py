"""
read the json files from data/raw/greenhouse and insert the data into raw table

what and how:
- we need to connect to postgrs
- for each company folder, we need to find that date's json file -> read it into dict -> converting each job into one row
- we create 2 functions: 1 read_raw --> it will read the data and get it off the disk
- And 2. to_row --> We give the shape to that data for table
"""

import sys
import json
from datetime import date
from pathlib import Path

import psycopg2  # pyright: ignore[reportMissingModuleSource]
from psycopg2.extras import Json  # pyright: ignore[reportMissingModuleSource]

RAW_DIR = Path("data/raw/greenhouse")
SOURCE = "greenhouse"
DB = {"host": "localhost",
      "port": 5434,
      "dbname": "jobs",
      "user": "jobs",
      "password": "jobs"
      }

DELETE_SQL =  """
delete from raw_job_postings
where load_date = %s and source = %s and company = %s
"""
INSERT_SQL = """
insert into raw_job_postings
(load_date, source, company, job_id, internal_job_id, title, location_name, updated_at, raw_json)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def read_raw(path: Path) -> dict:
    # read one raw json file and convert it into a python dict.
    with open(path) as f:  # similar to with open(path, 'r) --> read 'r' is a default, hence optional
        return json.load(f)
    #json.load reads the json text from a file and put it into dic
    #json.dump - reads the dic and put it into a json file


def to_rows(payload: dict, company: str, run_date: str)-> list[tuple]:
    #convert one API payload into one tuple per job in table column order
    rows = []

    for job in payload["jobs"]:
        location = job.get("location") or {}
        internal_id = job.get("internal_job_id")
        rows.append((
            run_date,
            SOURCE,
            company,
            str(job["id"]),
            str(internal_id) if internal_id is not None else None,
            job.get("title"),
            location.get("name"),
            job.get("updated_at"),
            Json(job)
        ))
    return rows


def load_board(conn: psycopg2.extensions.connection, company: str, run_date: str, rows: list[tuple])-> None:
    #replace one company's rows for one date : delete and then insert in one transaction
    with conn:                                      #wraps everything in one transaction, if any error, rollback everything
        with conn.cursor() as cur:
            cur.execute(DELETE_SQL, (run_date, SOURCE, company))
            cur.executemany(INSERT_SQL, rows)

def main():
    run_date = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    conn = psycopg2.connect(**DB)
    total = 0

    for folder in sorted(RAW_DIR.iterdir()):
        if not folder.is_dir():
            continue
        path = folder / f"{run_date}.json"
        if not path.exists():
            print(f"skip {folder.name}: no file for {run_date}")
            continue

        rows = to_rows(read_raw(path), folder.name, run_date)
        load_board(conn, folder.name, run_date, rows)
        print(f" OK {folder.name}: {len(rows)} rows loaded for {run_date}")

        total += len(rows)

    conn.close()
    print(f"\nDone: {total} rows loaded for {run_date}")

if __name__ == "__main__":
    main()







