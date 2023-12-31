from django.urls import path
from . import views

urlpatterns = [
    path("add_invoice/", views.add_invoice, name="add_invoice"),
    path("show_invoices/", views.show_invoices, name="show_invoices"),
    path("update_invoice/<int:id>", views.update_invoice, name="update_invoice"),
]
