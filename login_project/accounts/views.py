from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, Materials
from accounts.models import Material


# ---------- AUTH ----------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- DASHBOARD ----------
def dashboard(request):
    return render(request, 'accounts/dashboard.html')



# ---------- PROFILE ----------
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


# ---------- PAGES ----------
@login_required
def home(request):
    return render(request, 'accounts/home.html')


@login_required
def about(request):
    return render(request, 'accounts/about.html')


@login_required
def services(request):
    return render(request, 'accounts/services.html')


@login_required
def projects(request):
    return render(request, 'accounts/project.html')


@login_required
def contact(request):
    return render(request, 'accounts/contact.html')


# ---------- ADD CEMENT ----------
@login_required
def add_cement(request):
    if request.method == 'POST':
        form = Materials(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cement_verity')
    else:
        form = Materials()

    return render(request, 'accounts/add_cement.html', {'form': form})


# ---------- SHOW CEMENT ----------
@login_required
def cement_verity(request):
    cements = Material.objects.all()
    return render(request, 'accounts/cement_verity.html', {'cements': cements })
