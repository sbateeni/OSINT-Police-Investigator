from playwright.sync_api import sync_playwright

def reverse_image_search(uploaded_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://images.google.com")

        page.click("text=البحث بالصورة")
        page.click("text=تحميل صورة")

        file_path = f"temp/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        input_elem = page.query_selector("input[type='file']")
        input_elem.set_input_files(file_path)

        page.wait_for_selector("h3")
        links = page.query_selector_all("h3")
        results = []
        for h in links[:10]:
            parent = h.evaluate_handle("node => node.parentElement")
            href = parent.get_attribute("href")
            if href:
                results.append(href)

        browser.close()
        return results
