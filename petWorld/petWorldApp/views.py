from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Create your views here.

def home(request):
    context = {"latest_question_list": ""}
    return render(request, "petWorld/home/home.html", context)

def produtos(request):
    context = {"latest_question_list": ""}
    return render(request, "petWorld/produtos/produtos.html", context)