from datetime import datetime


def get_current_date(row_date):
    reverse_date = datetime.strptime(row_date, "%d-%m-%Y").strftime("%Y-%m-%d")
    date_to_db = datetime.strptime(reverse_date, "%Y-%m-%d").date()
    return date_to_db
