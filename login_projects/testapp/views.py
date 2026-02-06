from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# REGISTER VIEW
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password1
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'testapp/register.html')


# LOGIN VIEW
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'testapp/login.html')


# LOGOUT VIEW
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')


# HOME (LOGIN REQUIRED)
@login_required(login_url='login')
def home(request):
    return render(request, 'testapp/home.html')
