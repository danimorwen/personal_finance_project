from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from user_profile.repositories.user_profile import CategoryRepository
from .models import Invoice
from .repositories.invoices import InvoicesRepository


def add_invoice(request):
    categories = CategoryRepository().get_all_categories()
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
    invoices = InvoicesRepository()

    all_invoices = invoices.get_all_invoices()

    paid_invoices = invoices.get_paid_invoices()

    past_due_invoices = invoices.get_past_due_invoices(all_invoices, paid_invoices)

    due_invoices = invoices.get_due_invoices(all_invoices, paid_invoices)

    future_invoices = invoices.get_future_invoices(
        all_invoices, past_due_invoices, paid_invoices, due_invoices
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
