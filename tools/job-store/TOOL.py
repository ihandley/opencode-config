import json
from pathlib import Path
from typing import Any, Dict, List


DATA_PATH = Path.home() / "code" / "github" / "opencode" / "data" / "job-coach" / "jobs.json"


def _load() -> Dict[str, Any]:
    if not DATA_PATH.exists():
        return {"jobs": []}
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: Dict[str, Any]) -> Dict[str, Any]:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data


def list_jobs() -> Dict[str, List[Dict[str, Any]]]:
    data = _load()
    return {"jobs": data.get("jobs", [])}


def get_job(job_id: str) -> Dict[str, Any]:
    data = _load()
    for job in data.get("jobs", []):
        if job.get("id") == job_id:
            return job
    return {}


def add_job(job: Dict[str, Any]) -> Dict[str, Any]:
    data = _load()
    data.setdefault("jobs", []).append(job)
    _save(data)
    return job


def update_job(job_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    data = _load()
    for i, job in enumerate(data.get("jobs", [])):
        if job.get("id") == job_id:
            data["jobs"][i] = {**job, **updates}
            _save(data)
            return data["jobs"][i]
    return {}


def delete_job(job_id: str) -> Dict[str, str]:
    data = _load()
    jobs = data.get("jobs", [])
    new_jobs = [job for job in jobs if job.get("id") != job_id]
    data["jobs"] = new_jobs
    _save(data)
    return {"deleted": job_id}