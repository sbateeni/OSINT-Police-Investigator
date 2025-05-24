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
        if not phone:
            st.error("الرجاء إدخال رقم هاتف")
        else:
            try:
                with st.spinner("جارٍ البحث عن معلومات الهاتف..."):
                    result = lookup_phone(phone)
                
                # عرض التحذيرات إذا وجدت
                if "تحذير" in result:
                    st.warning(result["تحذير"])
                
                # عرض الأخطاء إذا وجدت
                if "خطأ" in result:
                    st.error(result["خطأ"])
                
                # عرض النتائج
                if "معلومات أساسية" in result and result["معلومات أساسية"]:
                    st.subheader("معلومات الهاتف:")
                    for key, value in result["معلومات أساسية"].items():
                        st.write(f"**{key}:** {value}")
                    
                    # عرض المصادر المستخدمة
                    if "مصادر" in result and result["مصادر"]:
                        st.write("**المصادر المستخدمة:**")
                        for source in result["مصادر"]:
                            st.write(f"- {source}")
                else:
                    st.info("لم يتم العثور على معلومات للرقم المحدد.")

                # البحث في وسائل التواصل الاجتماعي
                with st.spinner("جارٍ محاولة ربط الرقم بمنصات التواصل الاجتماعي..."):
                    links = check_social_media_by_phone(phone)
                if links:
                    st.subheader("روابط قد تكون مرتبطة بالرقم:")
                    for link in links:
                        st.write(link)
                else:
                    st.info("لم يتم العثور على ارتباطات واضحة عبر المواقع الاجتماعية.")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء البحث: {str(e)}")

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
