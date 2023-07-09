import os

from datetime import datetime
from io import BytesIO
from weasyprint import HTML

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import FileResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from user_profile.repositories.user_profile import AccountRepository, CategoryRepository
from .models import Transactions
from statement.repositories.statement import TransactionsRepository
from .utils import get_date


def transactions(request):
    if request.method == "GET":
        accounts = AccountRepository().get_all_accounts()
        categories = CategoryRepository().get_all_categories()
        return render(
            request,
            "transaction.html",
            {"accounts": accounts, "categories": categories},
        )

    elif request.method == "POST":
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        description = request.POST.get("description")
        date = request.POST.get("date")
        account = request.POST.get("account")
        type = request.POST.get("type")

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
            account = AccountRepository().get_account_by_id(account)
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
    accounts = AccountRepository().get_all_accounts
    categories = CategoryRepository().get_all_categories()

    account_get = request.GET.get("account")
    category_get = request.GET.get("category")
    date_range = request.GET.get("date_range")

    if account_get:
        transactions = transactions.filter(account__id=account_get)

    if category_get:
        transactions = transactions.filter(category__id=category_get)

    if date_range:
        transactions = transactions.filter(date__gte=get_date(date_range))

    if not date_range:
        transactions = transactions.filter(date__month=datetime.now().month)

    return render(
        request,
        "transactions_views.html",
        {
            "transactions": transactions,
            "accounts": accounts,
            "categories": categories,
        },
    )


def clear_filter(request):
    return redirect("/statement/transactions_views/")


def transactions_export(request):
    transactions = TransactionsRepository().get_transactions_for_current_month()
    statement_path = os.path.join(
        settings.BASE_DIR, "templates/partials/statement.html"
    )
    rendered_html = render_to_string(statement_path, {"transactions": transactions})
    output_path = BytesIO()
    HTML(string=rendered_html).write_pdf(output_path)
    output_path.seek(0)
    return FileResponse(output_path, filename="statement.pdf")
