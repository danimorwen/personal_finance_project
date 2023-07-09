import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from user_profile.repositories.user_profile import CategoryRepository


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
    # income bar
    categories = CategoryRepository().get_categories_by_expenses()
    return render(request, "planning_views.html", {"categories": categories})
