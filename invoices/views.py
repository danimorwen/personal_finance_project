from django.shortcuts import render
from user_profile.models import Category


def add_invoice(request):
    categories = Category.objects.all()
    if request.method == "GET":
        return render(request, "add_invoice.html", {"categories": categories})
