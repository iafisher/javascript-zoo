from django.urls import path

from . import views


app_name = "ui"

urlpatterns = [
    path("svelte", views.svelte_home, name="svelte_home"),
    path("vanilla", views.vanilla_home, name="vanilla_home")
]
