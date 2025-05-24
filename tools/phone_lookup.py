from playwright.sync_api import sync_playwright
import requests
import json
import os
import subprocess
import sys
import time

def install_playwright_browsers():
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        return True
    except Exception as e:
        print(f"Failed to install Playwright browsers: {str(e)}")
        return False

def lookup_phone(phone_number):
    results = {
        "معلومات أساسية": {},
        "مصادر": []
    }
    
    # تنظيف رقم الهاتف
    phone_number = phone_number.strip().replace(" ", "")
    
    # محاولة الحصول على معلومات من API مجاني
    try:
        api_url = f"https://api.numlookupapi.com/v1/validate/{phone_number}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results["معلومات أساسية"]["صالح"] = data.get("valid", "غير معروف")
            results["معلومات أساسية"]["البلد"] = data.get("country_name", "غير معروف")
            results["معلومات أساسية"]["المشغل"] = data.get("carrier", "غير معروف")
            results["مصادر"].append("NumLookupAPI")
    except Exception as e:
        results["تحذير"] = f"خطأ في استعلام API: {str(e)}"

    # محاولة البحث باستخدام Playwright
    try:
        with sync_playwright() as p:
            # استخدام chromium في وضع headless مع إعدادات خاصة للسحابة
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu'
                ]
            )
            
            context = browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            
            page = context.new_page()
            
            # البحث في sync.me
            url = f"https://sync.me/search/{phone_number}"
            try:
                page.goto(url, timeout=30000)  # زيادة وقت الانتظار إلى 30 ثانية
                page.wait_for_load_state('networkidle')
                
                # انتظار تحميل المحتوى
                time.sleep(5)
                
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
                results["تحذير"] = f"خطأ في استخراج المعلومات من Sync.me: {str(e)}"
            finally:
                context.close()
                browser.close()
                
    except Exception as e:
        results["تحذير"] = f"خطأ في تشغيل Playwright: {str(e)}"
    
    return results
