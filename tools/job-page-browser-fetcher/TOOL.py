import re
from typing import Any, Dict

from playwright.sync_api import sync_playwright


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_job_page_browser(url: str) -> Dict[str, Any]:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)

            title = _clean_text(page.title() or "")
            text = _clean_text(page.locator("body").inner_text())

            browser.close()

            return {
                "ok": True,
                "url": url,
                "title": title,
                "text": text,
                "error": "",
            }
    except Exception as e:
        return {
            "ok": False,
            "url": url,
            "title": "",
            "text": "",
            "error": str(e),
        }