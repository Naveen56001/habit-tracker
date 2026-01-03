from datetime import datetime
import pytz

def format_date_time():
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    return now_ist

def ist_date():
    now_ist = format_date_time()
    return now_ist.date()

def ist_time():
    now_ist = format_date_time()
    return now_ist.time()