from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def homepage(request):
    context = {}
    return render(request, "core/homepage.html", context)


@login_required
def user_view(request):
    user = request.user
    return render(request, "core/user.html", {"user": user})
