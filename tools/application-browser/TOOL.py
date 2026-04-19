from typing import Any, Dict, List
from playwright.sync_api import sync_playwright


def fill_application_form(
    url: str,
    fields: Dict[str, str],
    resume_path: str = "",
    cover_letter_path: str = "",
    dry_run: bool = True,
) -> Dict[str, Any]:
    actions: List[str] = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)

            for label, value in fields.items():
                filled = False

                selectors = [
                    f'input[name="{label}"]',
                    f'textarea[name="{label}"]',
                    f'input[id="{label}"]',
                    f'textarea[id="{label}"]',
                ]

                for selector in selectors:
                    loc = page.locator(selector)
                    if loc.count() > 0:
                        loc.first.fill(value)
                        actions.append(f'filled field: {label}')
                        filled = True
                        break

                if not filled:
                    actions.append(f'could not fill field: {label}')

            if resume_path:
                file_inputs = page.locator('input[type="file"]')
                if file_inputs.count() > 0:
                    file_inputs.first.set_input_files(resume_path)
                    actions.append("uploaded resume")
                else:
                    actions.append("could not find file input for resume")

            if cover_letter_path:
                file_inputs = page.locator('input[type="file"]')
                if file_inputs.count() > 1:
                    file_inputs.nth(1).set_input_files(cover_letter_path)
                    actions.append("uploaded cover letter")
                else:
                    actions.append("could not find second file input for cover letter")

            if dry_run:
                actions.append("dry run enabled; did not submit form")

            return {
                "ok": True,
                "url": url,
                "actions": actions,
                "error": "",
            }

    except Exception as e:
        return {
            "ok": False,
            "url": url,
            "actions": actions,
            "error": str(e),
        }