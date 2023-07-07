import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user_profile.models import Category


def create_planning(request):
    categories = Category.objects.all()
    return render(request, "create_planning.html", {"categories": categories})


@csrf_exempt
def update_category_limit(request, id):
    new_amount = json.load(request).get("new_amount")
    category = Category.objects.get(id=id)
    category.limit = new_amount
    category.save()
    return JsonResponse({"response": "success"})
