from playwright.sync_api import sync_playwright

def lookup_phone(phone_number):
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # مثال على موقع مجاني لفحص الرقم (sync.me)
        url = f"https://sync.me/search/{phone_number}"

        page.goto(url)
        page.wait_for_timeout(3000)  # الانتظار لثواني حتى تحميل الصفحة

        try:
            # محاولة التقاط اسم صاحب الرقم أو أي معلومات
            name = page.query_selector("h1")  # عنصر عنوان الصفحة (مثلاً الاسم)
            if name:
                results["الاسم"] = name.inner_text().strip()
            else:
                results["الاسم"] = "غير متوفر"

            # محاولة التقاط الموقع أو غيرها من المعلومات
            info = page.query_selector(".info")
            if info:
                results["معلومات إضافية"] = info.inner_text().strip()

        except Exception as e:
            results["خطأ"] = f"لم يتمكن من استخراج المعلومات: {str(e)}"

        browser.close()
    return results
