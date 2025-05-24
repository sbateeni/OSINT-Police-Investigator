from playwright.sync_api import sync_playwright

def check_social_media_by_phone(phone_number):
    search_engines = [
        f"https://www.google.com/search?q={phone_number}+site:facebook.com",
        f"https://www.google.com/search?q={phone_number}+site:instagram.com",
        f"https://www.google.com/search?q={phone_number}+site:twitter.com",
        f"https://www.google.com/search?q={phone_number}+site:tiktok.com",
        f"https://www.google.com/search?q={phone_number}+site:linkedin.com",
        f"https://www.google.com/search?q={phone_number}+site:pinterest.com",
        f"https://www.google.com/search?q={phone_number}+site:snapchat.com",
        f"https://www.google.com/search?q={phone_number}+site:reddit.com",
        f"https://www.google.com/search?q={phone_number}+site:youtube.com",
        f"https://www.google.com/search?q={phone_number}+site:ask.fm"
    ]
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for url in search_engines:
            page.goto(url)
            page.wait_for_timeout(2000)
            anchors = page.query_selector_all("a")
            for a in anchors:
                href = a.get_attribute("href")
                if href and phone_number in href:
                    results.append(href)
        browser.close()
    return list(set(results))
