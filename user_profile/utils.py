from datetime import datetime
from django.db.models import Sum


def sum_total(object, field):
    return object.aggregate(Sum(field))[f"{field}__sum"]


def get_total_expenses_by_category(categories, transactions):
    present_month = datetime.now().month

    months = {
        1: "JAN",
        2: "FEB",
        3: "MAR",
        4: "APR",
        5: "MAY",
        6: "JUN",
        7: "JUL",
        8: "AUG",
        9: "SEP",
        10: "OCT",
        11: "NOV",
        12: "DEC",
    }
    data = {}
    for category in categories:
        value_list = []
        for number in months.keys():
            if number > present_month:
                break
            sum_by_category = sum_total(
                transactions.filter(category=category).filter(date__month=number),
                "amount",
            )
            if sum_by_category:
                value_list.append(sum_by_category)
            else:
                value_list.append(0)
        data[category.name] = value_list

    return data
