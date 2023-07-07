from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def get_date(date_range_str):
    date_filter = date_range_str.split()
    print(date_filter)
    date = datetime.today().date() - relativedelta(month=1)
    if date_filter[2] == "days":
        date = datetime.today().date() - relativedelta(days=int(date_filter[1]))

    elif date_filter[2] == "months":
        date = datetime.today().date() - relativedelta(months=int(date_filter[1]))

    elif date_filter[2] == "years":
        date = datetime.today().date() - relativedelta(years=int(date_filter[1]))

    return date
