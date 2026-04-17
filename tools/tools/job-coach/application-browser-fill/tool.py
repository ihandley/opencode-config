from playwright.sync_api import sync_playwright
import time

def try_fill(page, selectors, value):
    for sel in selectors:
        try:
            locator = page.locator(sel).first
            if locator.count() == 0:
                continue

            locator.scroll_into_view_if_needed()
            locator.click()
            locator.fill("")
            locator.fill(value)

            # verify
            current = locator.input_value()
            if current.strip() == value.strip():
                return {"ok": True, "selector": sel}

            # fallback: JS injection
            locator.evaluate("""
                (el, val) => {
                    el.value = val;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """, value)

            current = locator.input_value()
            if current.strip() == value.strip():
                return {"ok": True, "selector": sel}

        except Exception:
            continue

    return {"ok": False, "selector": ""}


def fill_application_form(data: dict):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        # --- Basic fields ---
        fields = [
            ("full_name", ["input[name='name']", "input[placeholder*='Name']"]),
            ("email", ["input[type='email']"]),
            ("phone", ["input[type='tel']"]),
        ]

        for key, selectors in fields:
            value = data.get(key, "")
            if not value:
                continue

            result = try_fill(page, selectors, value)
            results.append({
                "field": key,
                "value": value,
                "status": result["ok"],
                "selector": result["selector"]
            })

        # --- Work experience (basic attempt) ---
        for job in data.get("work_experience", []):
            result = try_fill(page, ["input[placeholder*='Company']"], job.get("company", ""))
            results.append({"field": "company", "value": job.get("company"), "status": result["ok"]})

            result = try_fill(page, ["input[placeholder*='Title']"], job.get("title", ""))
            results.append({"field": "title", "value": job.get("title"), "status": result["ok"]})

        return {
            "status": "completed",
            "results": results
        }