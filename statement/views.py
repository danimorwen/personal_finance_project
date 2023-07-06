from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from user_profile.models import Account, Category
from .models import Transactions


def transactions(request):
    if request.method == "GET":
        accounts = Account.objects.all()
        categories = Category.objects.all()
        return HttpResponse(
            render(
                request,
                "transaction.html",
                {"accounts": accounts, "categories": categories},
            )
        )
    elif request.method == "POST":
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        description = request.POST.get("description")
        date = request.POST.get("date")
        account = request.POST.get("account")
        type = request.POST.get("type")
        print("Dados recebidos:", amount, category, description, date, account, type)

        if amount == "0" or len(amount) == 0:
            messages.add_message(
                request, constants.ERROR, "Amount must be a number greater than 0"
            )
        elif len(description.strip()) == 0:
            messages.add_message(
                request, constants.ERROR, "Description must have at least one character"
            )
        elif len(date) == 0:
            messages.add_message(request, constants.ERROR, "Invalid date")
        elif len(type) == 0:
            messages.add_message(
                request, constants.ERROR, "You must choose a type of transaction"
            )
        else:
            transaction = Transactions(
                amount=amount,
                category_id=category,
                description=description,
                date=date,
                account_id=account,
                type=type,
            )
            transaction.save()
            account = Account.objects.get(id=account)
            print("type", type)
            if type == "I":
                account.amount += float(amount)
                messages.add_message(
                    request, constants.SUCCESS, f"Income added successfully!"
                )

            else:
                account.amount -= float(amount)
                messages.add_message(
                    request, constants.SUCCESS, f"Expense added successfully!"
                )
            account.save()

        return redirect("/statement/transactions")


def transactions_views(request):
    transactions = Transactions.objects.all()

    return HttpResponse(
        render(
            request,
            "transactions_views.html",
            {
                "transactions": transactions,
            },
        )
    )
