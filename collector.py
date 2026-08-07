import json
import urllib.request
from datetime import datetime

API_URL = "https://remotive.com/api/remote-jobs"

def fetch_jobs():
    print("Fetching remote jobs from Remotive...")

    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data.get("jobs", [])


def normalize_job(job):
    return {
        "id": job.get("id"),
        "company": job.get("company_name"),
        "title": job.get("title"),
        "category": job.get("category"),
        "job_type": job.get("job_type"),
        "location": job.get("candidate_required_location"),
        "salary": job.get("salary"),
        "published_date": job.get("publication_date"),
        "url": job.get("url"),
        "description": job.get("description")
    }


def remove_duplicates(jobs):
    seen = set()
    unique_jobs = []

    for job in jobs:
        key = job.get("url")

        if key and key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs


def save_jobs(jobs):
    output = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_jobs": len(jobs),
        "jobs": jobs
    }

    with open("jobs.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2, ensure_ascii=False)

    print(f"Saved {len(jobs)} jobs to jobs.json")


if __name__ == "__main__":
    raw_jobs = fetch_jobs()

    print(f"API returned {len(raw_jobs)} jobs.")

    normalized_jobs = [
        normalize_job(job)
        for job in raw_jobs
    ]

    unique_jobs = remove_duplicates(normalized_jobs)

    save_jobs(unique_jobs)
