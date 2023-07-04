from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("management/", views.management, name="management"),
    path("create_bank_account", views.create_bank_account, name="create_bank_account"),
]
