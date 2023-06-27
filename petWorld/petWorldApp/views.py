from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .models import Category, Product

# Create your views here.

product_titles = { "Dogs": "Catioros", 
                  "Cats": "Gatíneos", 
                  "Peixes": "Peixes", 
                  "Aves": "Aves", 
                  "Roedores": "Roedores" }
product_img_names = { "Dogs": "figure-6-cartoon-dog.png", 
                "Cats": "figure-6-cartoon-dog.png", 
                "Peixes": "figure-6-cartoon-dog.png", 
                "Aves": "figure-6-cartoon-dog.png", 
                "Roedores": "figure-6-cartoon-dog.png" }
product_imgs_alts = { "Dogs": "Figura de um cachorro segurando um disco com a boca", 
                "Cats": "Figura de um cachorro segurando um disco com a boca", 
                "Peixes": "Figura de um cachorro segurando um disco com a boca", 
                "Aves": "Figura de um cachorro segurando um disco com a boca", 
                "Roedores": "Figura de um cachorro segurando um disco com a boca" }

def home(request):
    context = {}
    return render(request, "petWorld/home/home.html", context)

def produtos(request, product_type):
    category = Category.objects.filter(name=product_type).first()
    
    products = []
    if category is not None:
        products = Product.objects.filter(categories__id=category.pk).all()
    
    categories = dict()
    for product in products:
        for category in product.categories.all():
            if category.name != product_type:
                if category.name in categories:
                    categories[category.name] += 1
                else:
                    categories[category.name] = 1
    
    context = {
        "product_title": product_titles[product_type],
        "product_img": "petWorld/figures/" + product_img_names[product_type],
        "product_img_alt": product_imgs_alts[product_type],
        "products": products,
        "categories": sorted(categories.items())
    }
    return render(request, "petWorld/produtos/produtos.html", context)

def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('/')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'cadastro.html', {'form_usuario': form_usuario})

def login_client(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, "petWorld/login/login.html", {'form_login': form_login})

def logout_request(request):
	logout(request) 
	return redirect("/")