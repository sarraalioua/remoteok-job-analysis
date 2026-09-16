import requests
import pandas as pd
import os

url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
print("Status code:", response.status_code)

response.raise_for_status()

data = response.json()

jobs = []

for job in data[1:]:
    jobs.append({
        "url": job.get("url"),
        "title": job.get("position"),
        "company": job.get("company"),
        "location": job.get("location") or "Remote",
        "remote": True,
        "job_type": "Remote",
        "salary": job.get("salary"),
        "date_posted": job.get("date"),
        "skills": ", ".join(job.get("tags", []))
    })

df = pd.DataFrame(jobs)

print(df.head())
print("Shape:", df.shape)

output_path = os.path.join(os.getcwd(), "jobs_data.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("CSV created here:")
print(output_path)
