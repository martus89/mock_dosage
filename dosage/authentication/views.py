from .forms import CustomUserCreationForm
from django.shortcuts import render
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
