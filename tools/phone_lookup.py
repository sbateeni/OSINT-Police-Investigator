from playwright.sync_api import sync_playwright
import requests
import json

def lookup_phone(phone_number):
    results = {
        "معلومات أساسية": {},
        "مصادر": []
    }
    
    # تنظيف رقم الهاتف
    phone_number = phone_number.strip().replace(" ", "")
    
    try:
        # محاولة الحصول على معلومات من API مجاني
        api_url = f"https://api.numlookupapi.com/v1/validate/{phone_number}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            results["معلومات أساسية"]["صالح"] = data.get("valid", "غير معروف")
            results["معلومات أساسية"]["البلد"] = data.get("country_name", "غير معروف")
            results["معلومات أساسية"]["المشغل"] = data.get("carrier", "غير معروف")
            results["مصادر"].append("NumLookupAPI")
    except Exception as e:
        results["خطأ"] = f"خطأ في استعلام API: {str(e)}"

    try:
        # محاولة البحث باستخدام Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # البحث في sync.me
            url = f"https://sync.me/search/{phone_number}"
            page.goto(url)
            page.wait_for_timeout(3000)
            
            try:
                name = page.query_selector("h1")
                if name:
                    results["معلومات أساسية"]["الاسم"] = name.inner_text().strip()
                else:
                    results["معلومات أساسية"]["الاسم"] = "غير متوفر"
                
                info = page.query_selector(".info")
                if info:
                    results["معلومات أساسية"]["معلومات إضافية"] = info.inner_text().strip()
                
                results["مصادر"].append("Sync.me")
            except Exception as e:
                results["خطأ"] = f"خطأ في استخراج المعلومات من Sync.me: {str(e)}"
            
            browser.close()
    except Exception as e:
        results["خطأ"] = f"خطأ في تشغيل Playwright: {str(e)}"
    
    return results
