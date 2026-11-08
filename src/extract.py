import requests

BOARD = "databricks"
URL = f"https://boards-api.greenhouse.io/v1/boards/{BOARD}/jobs"

response = requests.get(URL, params={"content": "true"}, timeout=30)
response.raise_for_status()

data = response.json()
jobs = data["jobs"]


# print(f"{BOARD}: {len(jobs)} jobs")

# for job in jobs[:5]:
#     print(job["id"], job["title"], job["location"]["name"])

ids = []
internal_ids = []


for job in jobs:
    ids.append(job["id"])
    internal_ids.append(job["internal_job_id"])


print("record:", len(ids))
print("distinct ids:", len(set(ids)))
print("distinct internal job id:", len(set(internal_ids)))

# print(type(ids), ids)