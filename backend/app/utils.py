from datetime import datetime

def parse_date(date_string):
    if not date_string:
        return None
    try:
        return datetime.fromisoformat(date_string)
    except ValueError:
        return None