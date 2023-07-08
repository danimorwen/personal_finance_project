from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from user_profile.models import Category
from .models import Invoice, PaidInvoice


def add_invoice(request):
    categories = Category.objects.all()
    if request.method == "GET":
        return render(request, "add_invoice.html", {"categories": categories})
    else:
        name = request.POST.get("name")
        category = request.POST.get("category")
        description = request.POST.get("description")
        amount = request.POST.get("amount")
        due_date = request.POST.get("due_date")
        recurring = bool(request.POST.get("recurring"))

        invoice = Invoice(
            name=name,
            category_id=category,
            description=description,
            amount=amount,
            due_date=due_date,
            recurring=recurring,
        )
        invoice.save()
        messages.add_message(request, constants.SUCCESS, "Invoice added successfully")
        return redirect("/invoices/add_invoice")


def show_invoices(request):
    present_month = datetime.now().month
    present_day = datetime.now().day

    invoices = Invoice.objects.all()

    paid_invoices = PaidInvoice.objects.filter(
        payment_date__month=present_month
    ).values("invoice")

    past_due_invoices = invoices.filter(due_date__lt=present_day).exclude(
        id__in=paid_invoices
    )

    due_invoices = (
        invoices.filter(due_date__lte=present_day + 5)
        .filter(due_date__gte=present_day)
        .exclude(id__in=paid_invoices)
    )

    future_invoices = (
        invoices.exclude(id__in=past_due_invoices)
        .exclude(id__in=paid_invoices)
        .exclude(id__in=due_invoices)
    )

    return render(
        request,
        "show_invoices.html",
        {
            "past_due_invoices": past_due_invoices,
            "due_invoices": due_invoices,
            "future_invoices": future_invoices,
        },
    )
