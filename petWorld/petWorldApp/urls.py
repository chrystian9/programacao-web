from django.urls import path

from . import views

app_name = "petWorld"
urlpatterns = [
    path("", views.home, name="home'"),
    path("produtos/<str:product_type>/", views.produtos, name="produtos"),
]