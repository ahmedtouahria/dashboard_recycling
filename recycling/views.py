from django.shortcuts import render

def home(request):
    context={}
    return render(request,"pages/index.html",context)

def register(request):
    context={}
    return render(request,"pages/sign_in.html",context)
def login_user(request):
    context={}
    return render(request,"pages/login.html",context)

def add(request):
    context={}
    return render(request,"pages/add.html",context)
