from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse(render(request, "home.html"))


def management(request):
    return HttpResponse(render(request, "management.html"))
