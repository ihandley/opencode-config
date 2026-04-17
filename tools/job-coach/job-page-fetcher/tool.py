import re
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_job_page(url: str) -> Dict[str, Any]:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
    except Exception as e:
        return {
            "ok": False,
            "url": url,
            "title": "",
            "text": "",
            "error": str(e),
        }

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = _clean_text(soup.title.get_text()) if soup.title else ""

    text = _clean_text(soup.get_text(separator=" "))

    return {
        "ok": True,
        "url": url,
        "title": title,
        "text": text,
        "error": "",
    }