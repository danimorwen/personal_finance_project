from django.urls import path
from . import views

urlpatterns = [
    path("transactions/", views.transactions, name="transactions"),
    path("transactions_views/", views.transactions_views, name="transactions_views"),
    path("clear_filter/", views.clear_filter, name="clear_filter"),
    path("transactions_export/", views.transactions_export, name="transactions_export"),
]
