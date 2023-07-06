from django.urls import path
from . import views

urlpatterns = [
    path("transactions/", views.transactions, name="transactions"),
    path("transactions_views/", views.transactions_views, name="transactions_views"),
]
