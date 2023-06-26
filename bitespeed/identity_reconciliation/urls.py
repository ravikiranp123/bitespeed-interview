from django.urls import path

from . import views

urlpatterns = [
    path("identify", views.identify, name="identify"),
    path("reset", views.reset, name="reset")
]