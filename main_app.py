import streamlit as st
from tools.phone_lookup import lookup_phone
from tools.social_phone_check import check_social_media_by_phone
from tools.image_reverse_search import reverse_image_search
from tools.email_lookup import lookup_email

st.set_page_config(page_title="البحث الشرطي الموحد", layout="centered")
st.title("نظام البحث المتكامل للمحققين")

input_type = st.radio("حدد نوع المعلومة المتوفرة لديك:", ["رقم هاتف", "بريد إلكتروني", "صورة"])

if input_type == "رقم هاتف":
    phone = st.text_input("أدخل رقم الهاتف (مع رمز الدولة):")
    if st.button("بحث"):
        with st.spinner("جارٍ البحث باستخدام PhoneInfoga..."):
            result = lookup_phone(phone)
        st.subheader("معلومات الهاتف:")
        st.code(result)

        with st.spinner("جارٍ محاولة ربط الرقم بمنصات التواصل الاجتماعي..."):
            links = check_social_media_by_phone(phone)
        if links:
            st.subheader("روابط قد تكون مرتبطة بالرقم:")
            for link in links:
                st.write(link)
        else:
            st.info("لم يتم العثور على ارتباطات واضحة عبر المواقع الاجتماعية.")

elif input_type == "بريد إلكتروني":
    email = st.text_input("أدخل البريد الإلكتروني:")
    if st.button("تحقق"):
        with st.spinner("جارٍ تحليل البريد..."):
            info = lookup_email(email)
        st.subheader("نتائج تحليل البريد الإلكتروني:")
        st.json(info)

elif input_type == "صورة":
    uploaded_file = st.file_uploader("ارفع صورة الوجه أو لقطة شاشة:", type=["png", "jpg", "jpeg"])
    if uploaded_file and st.button("بحث عكسي"):
        with st.spinner("جارٍ تنفيذ بحث عكسي باستخدام Google..."):
            image_results = reverse_image_search(uploaded_file)
        if image_results:
            st.subheader("روابط مشابهة أو تطابقات للصور:")
            for link in image_results:
                st.write(link)
        else:
            st.info("لم يتم العثور على تطابقات للصورة.")
