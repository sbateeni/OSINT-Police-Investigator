from email_validator import validate_email as ve, EmailNotValidError

def lookup_email(email):
    try:
        basic = ve(email, check_deliverability=False)
        domain = basic["domain"]
        return {
            "صالح": True,
            "النطاق": domain,
            "تفاصيل": basic
        }
    except EmailNotValidError as e:
        return {"صالح": False, "خطأ": str(e)}
