from django.db.models import Sum


def sum_total(object, field):
    return object.aggregate(Sum(field))[f"{field}__sum"]
