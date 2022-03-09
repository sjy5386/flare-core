from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from .decorators import logout_required


@login_required
@require_GET
def profile(request: HttpRequest):
    return render(request, 'accounts/profile.html')


@logout_required
def register(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'accounts/register.html', {
            'form': UserCreationForm()
        })
    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return HttpResponse('Your password does not match.')
        user = get_user_model().objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect(reverse('profile'))
