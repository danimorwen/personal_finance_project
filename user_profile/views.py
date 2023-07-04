from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, Category


def home(request):
    return HttpResponse(render(request, "home.html"))


def management(request):
    return HttpResponse(render(request, "management.html"))


def create_bank_account(request):
    name = request.POST.get("name")
    bank = request.POST.get("bank")
    type = request.POST.get("type")
    amount = request.POST.get("amount")
    icon = request.FILES.get("icon")
    if len(name.strip()) == 0 or not amount.isdigit():
        return redirect("/profile/management")

    account = Account(name=name, bank=bank, type=type, amount=amount, bank_icon=icon)
    account.save()
    return redirect("/profile/management")
