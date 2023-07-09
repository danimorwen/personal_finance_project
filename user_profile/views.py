from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants


from .models import Account, Category
from .repositories.user_profile import AccountRepository, CategoryRepository
from statement.repositories.statement import TransactionsRepository
from invoices.repositories.invoices import InvoicesRepository
from .utils import (
    sum_total,
    get_total_expenses_by_category,
    get_expenses_percentage_by_essential,
)


def home(request):
    accounts = AccountRepository()
    all_accounts = accounts.get_all_accounts()
    total_amount = sum_total(all_accounts, "amount")
    transactions = TransactionsRepository()
    monthly_transactions = transactions.get_transactions_for_current_month()
    income = sum_total(transactions.get_filtered_income(monthly_transactions), "amount")
    expenses = sum_total(
        transactions.get_filtered_expenses(monthly_transactions), "amount"
    )
    (
        essential_percentage,
        non_essential_percentage,
    ) = get_expenses_percentage_by_essential(monthly_transactions)
    invoices = InvoicesRepository()
    all_invoices = invoices.get_all_invoices()
    paid_invoices = invoices.get_paid_invoices()
    past_due_invoices = invoices.get_past_due_invoices(all_invoices, paid_invoices)
    due_invoices = invoices.get_due_invoices(all_invoices, paid_invoices)
    total_monthly = income - expenses

    return HttpResponse(
        render(
            request,
            "home.html",
            {
                "accounts": all_accounts,
                "total_amount": total_amount,
                "income": income,
                "expenses": expenses,
                "essential_percentage": essential_percentage,
                "non_essential_percentage": non_essential_percentage,
                "past_due_invoices": len(past_due_invoices),
                "due_invoices": len(due_invoices),
                "total_monthly": total_monthly,
            },
        )
    )


def management(request):
    accounts = AccountRepository().get_all_accounts()
    total_amount = sum_total(accounts, "amount")
    categories = CategoryRepository().get_all_categories()
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
    account = AccountRepository().get_account_by_id(id)
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
    category = CategoryRepository().get_category_by_id(id)
    category.essential = not category.essential
    category.save()
    return redirect("/profile/management")


def dashboard(request):
    categories = CategoryRepository().get_categories_by_expenses()
    transactions = TransactionsRepository().get_all_expenses()
    data = get_total_expenses_by_category(categories, transactions)

    return render(
        request,
        "dashboard.html",
        {"expenses_by_category": data},
    )
