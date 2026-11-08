import json
from datetime import date
from pathlib import Path

import requests

BOARDS = ["gitlab", "databricks", "stripe", "testcompany"]
BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
RAW_DIR = Path("data/raw/greenhouse")


"""func to call api for one board and return the json respose"""
def fetch_board(board:str) -> dict:
    url = BASE_URL.format(board = board)
    response = requests.get(url, params={"content": "true"}, timeout=30)
    response.raise_for_status()
    return response.json()

def save_raw(board: str, payload: dict, run_date: str) -> Path:
    folder = RAW_DIR/board
    folder.mkdir(parents=True, exist_ok=True)
    path = folder/f"{run_date}.json"

    with open(path, "w") as f:
        #json.dump taked in 2 param - (what to write, where to write)
        json.dump(payload, f)
    return path

def main():
    run_date = date.today().isoformat()
    succeeded, failed = [], []

    for board in BOARDS:
        try:
            payload = fetch_board(board)
            path = save_raw(board, payload, run_date)
            print(f"{board}: {len(payload['jobs'])} jobs -> {path}")
            succeeded.append(board)
        except requests.RequestException as error:
            print(f"FAIL {board}: {error}")
            failed.append(board)

    print(f"Done: {len(succeeded)} succeeded, {len(failed)} failed")

if __name__ == "__main__":
    main()

    





##-- EXTRACTING ONE JOB TO TEST---
# BOARD = "databricks"
# URL = f"https://boards-api.greenhouse.io/v1/boards/{BOARD}/jobs"

# response = requests.get(URL, params={"content": "true"}, timeout=30)
# response.raise_for_status()

# data = response.json()
# jobs = data["jobs"]


# # print(f"{BOARD}: {len(jobs)} jobs")

# # for job in jobs[:5]:
# #     print(job["id"], job["title"], job["location"]["name"])

# ids = []
# internal_ids = []


# for job in jobs:
#     ids.append(job["id"])
#     internal_ids.append(job["internal_job_id"])


# print("record:", len(ids))
# print("distinct ids:", len(set(ids)))
# print("distinct internal job id:", len(set(internal_ids)))

# # print(type(ids), ids)