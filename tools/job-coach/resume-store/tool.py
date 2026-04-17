import json
from pathlib import Path
from typing import Any, Dict


DATA_PATH = Path.home() / "code" / "github" / "opencode" / "data" / "job-coach" / "resume.json"


def _save(data: Dict[str, Any]) -> Dict[str, Any]:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data


def _load() -> Dict[str, Any]:
    if not DATA_PATH.exists():
        return {}
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_resume(resume: Dict[str, Any]) -> Dict[str, Any]:
    return _save(resume)


def get_resume() -> Dict[str, Any]:
    return _load()