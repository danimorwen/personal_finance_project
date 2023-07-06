from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants

from .models import Account, Category
from .utils import sum_total


def home(request):
    accounts = Account.objects.all()
    total_amount = sum_total(accounts, "amount")
    return HttpResponse(
        render(
            request,
            "home.html",
            {
                "accounts": accounts,
                "total_amount": total_amount,
            },
        )
    )


def management(request):
    accounts = Account.objects.all()
    total_amount = sum_total(accounts, "amount")
    categories = Category.objects.all()
    return HttpResponse(
        render(
            request,
            "management.html",
            {
                "accounts": accounts,
                "total_amount": total_amount,
                "categories": categories,
            },
        )
    )


def create_bank_account(request):
    name = request.POST.get("name")
    bank = request.POST.get("bank")
    type = request.POST.get("type")
    amount = request.POST.get("amount")
    icon = request.FILES.get("icon")

    if len(name.strip()) == 0:
        messages.add_message(
            request, constants.ERROR, "Name should hava at least on character"
        )

    elif not amount.isdigit() or len(amount) == 0:
        messages.add_message(request, constants.ERROR, "Amount should be a number")

    else:
        account = Account(
            name=name, bank=bank, type=type, amount=amount, bank_icon=icon
        )
        account.save()
        messages.add_message(
            request, constants.SUCCESS, "Account created successfully!"
        )

    return redirect("/profile/management")


def delete_bank_account(request, id):
    account = Account.objects.get(id=id)
    account.delete()
    messages.add_message(request, constants.SUCCESS, "Account deleted successfully!")
    return redirect("/profile/management")


def create_category(request):
    name = request.POST.get("name")
    essential = bool(request.POST.get("essential"))

    if len(name.strip()) == 0:
        messages.add_message(
            request, constants.ERROR, "Name should have at least 1 character"
        )
        return redirect("/profile/management")
    category = Category(name=name, essential=essential)
    category.save()
    messages.add_message(request, constants.SUCCESS, "Category created successfully!")
    return redirect("/profile/management")


def update_category(request, id):
    category = Category.objects.get(id=id)
    category.essential = not category.essential
    category.save()
    return redirect("/profile/management")
