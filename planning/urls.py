from django.urls import path
from . import views

urlpatterns = [
    path("create_planning/", views.create_planning, name="create_planning"),
    path(
        "update_category_limit/<int:id>",
        views.update_category_limit,
        name="update_category_limit",
    ),
    path("planning_views/", views.planning_views, name="planning_views"),
]
