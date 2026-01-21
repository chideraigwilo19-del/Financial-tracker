from datetime import datetime

CATEGORIES = [
    "Food", "Transport", "Bills", "Shopping", "Health",
    "Entertainment", "Education", "Salary", "Other"
]

def validate_amount(value):
    try:
        float(value)
        return True
    except:
        return False

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")