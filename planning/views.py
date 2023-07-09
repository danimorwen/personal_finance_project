import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from user_profile.repositories.user_profile import CategoryRepository
from statement.repositories.statement import TransactionsRepository
from user_profile.utils import sum_total


def create_planning(request):
    categories = CategoryRepository().get_all_categories()
    return render(request, "create_planning.html", {"categories": categories})


@csrf_exempt
def update_category_limit(request, id):
    new_amount = json.load(request).get("new_amount")
    category = CategoryRepository().get_category_by_id(id)
    category.limit = new_amount
    category.save()
    return JsonResponse({"response": "success"})


def planning_views(request):
    income_limit = CategoryRepository().get_category_by_name("Salary")[0].limit
    categories = CategoryRepository().get_categories_by_expenses()
    transactions = TransactionsRepository()
    current_month_transactions = transactions.get_transactions_for_current_month()
    current_month_expenses = sum_total(
        transactions.get_filtered_expenses(current_month_transactions), "amount"
    )
    available_income = income_limit - current_month_expenses
    available_income_percentage = int(available_income / income_limit * 100)
    print(available_income_percentage)
    return render(
        request,
        "planning_views.html",
        {
            "categories": categories,
            "income_limit": income_limit,
            "available_income": available_income,
            "available_income_percentage": available_income_percentage,
        },
    )
