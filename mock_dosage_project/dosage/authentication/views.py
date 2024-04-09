from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def registration_form(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Thanks! Your registration has been successful")
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('login_success')
        else:
            messages.add_message(request, messages.SUCCESS, f"Uh oh! Wrong username/password.")
    return render(request, 'authentication/login.html')


@login_required
def login_success(request):
    messages.add_message(request, messages.SUCCESS, f"Hello {request.user.name}! You are logged in now.")
    return render(request, 'authentication/login_success.html')


def logout_page(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "You have been logged out. Bye!")
    return render(request, 'authentication/logout.html')
