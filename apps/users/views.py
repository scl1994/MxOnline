# coding=utf-8

from django.shortcuts import render
from django.contrib.auth import authenticate, login

# Create your views here.


def login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(user_name, pass_word)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, "index.html", {})
    return render(request, "login.html", {})
