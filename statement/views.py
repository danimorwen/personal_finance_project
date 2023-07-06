from django.shortcuts import render
from user_profile.models import Account, Category


def transactions(request):
    if request.method == "GET":
        accounts = Account.objects.all()
        categories = Category.objects.all()
        return render(
            request,
            "transactions.html",
            {"accounts": accounts, "categories": categories},
        )
