from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('chat')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('chat')

    return render(request, 'accounts/login.html')