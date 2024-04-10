from .forms import CustomUserCreationForm
from django.shortcuts import render
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


@login_required
def login_success(request):
    messages.add_message(request, messages.SUCCESS, f"Hello {request.user.name}! You are logged in now.")
    return render(request, 'authentication/login_success.html')
