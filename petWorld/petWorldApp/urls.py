from django.urls import path

from . import views

app_name = "petWorld"
urlpatterns = [
    path("", views.home, name="home'"),
    path("produtos/<str:product_type>/", views.produtos, name="produtos"),
    path("login/", views.login_client, name="login"),
    path("logout/", views.logout_client, name="logout"),
    path("cadastrar/", views.cadastrar_usuario, name="logout"),
    path("carrinho/", views.carrinho, name="carrinho"),
    path("adicionar-ao-carrinho/<int:produto_id>", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho")
]