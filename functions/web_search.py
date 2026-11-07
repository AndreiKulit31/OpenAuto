from playwright.sync_api import sync_playwright
from yt_dlp import YoutubeDL


def search_web(query="", limit=5):
    if not query.strip():
        return []

    results = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(
                "https://www.google.com/search",
                wait_until="domcontentloaded",
                timeout=30000,
            )

            page.locator("textarea[name='q'], input[name='q']").first.fill(query)
            page.keyboard.press("Enter")

            page.wait_for_load_state("domcontentloaded")

            search_results = page.locator("div.MjjYud").all()

            for item in search_results[:limit]:
                title = item.locator("h3").first
                link = item.locator("a").first

                if title.count() and link.count():
                    results.append({
                        "title": title.inner_text(),
                        "url": link.get_attribute("href"),
                        "snippet": item.inner_text(),
                    })

        finally:
            browser.close()

    return results


def search_videos(query="", limit=5):
    if not query.strip():
        return []

    options = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
    }

    with YoutubeDL(options) as ydl:
        data = ydl.extract_info(
            f"ytsearch{limit}:{query}",
            download=False,
        )

    return [
        {
            "title": video.get("title"),
            "url": video.get("url") or video.get("webpage_url"),
            "duration": video.get("duration"),
        }
        for video in data.get("entries", [])
    ]