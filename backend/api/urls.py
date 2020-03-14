from django.urls import path

from . import views


app_name = "api"

urlpatterns = [
    path("task/create", views.create_task, name="create_task"),
    path(
        "task/update/description",
        views.update_task_description,
        name="update_task_description",
    ),
    path("task/update/status", views.update_task_status, name="update_task_status"),
    path("task/delete", views.delete_task, name="delete_task"),
    path("project/create", views.create_project, name="create_project"),
    path(
        "project/update/description",
        views.update_project_description,
        name="update_project_description",
    ),
    path("project/delete", views.delete_project, name="delete_project"),
]
