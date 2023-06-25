from django.urls import path

from . import views

app_name = "petWorld"
urlpatterns = [
    path("", views.home, name="home'"),
    path("produtos/", views.produtos, name="produtos"),
]