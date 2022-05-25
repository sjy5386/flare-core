from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from .decorators import logout_required
from .forms import UserRegisterForm, CaptchaForm


@login_required
@require_GET
def profile(request: HttpRequest):
    return render(request, 'accounts/profile.html')


@logout_required
def register(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'accounts/register.html', {
            'form': UserRegisterForm(),
            'captcha_form': CaptchaForm()
        })
    elif request.method == 'POST':
        captcha = CaptchaForm(request.POST).is_valid()
        if not captcha:
            messages.add_message(request, messages.ERROR, captcha)
            return redirect('register')
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.add_message(request, messages.ERROR, 'Your password does not match.')
            return redirect('register')
        email = request.POST['email']
        user = get_user_model().objects.create_user(username=username, password=password1, email=email)
        login(request, user)
        return redirect(reverse('profile'))
