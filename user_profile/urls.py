from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("management/", views.management, name="management"),
    path("create_bank_account", views.create_bank_account, name="create_bank_account"),
    path(
        "delete_bank_account/<int:id>",
        views.delete_bank_account,
        name="delete_bank_account",
    ),
    path("create_category", views.create_category, name="create_category"),
    path("update_category/<int:id>", views.update_category, name="update_category"),
]
