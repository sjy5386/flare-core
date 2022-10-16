from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth

from .decorators import logout_required
from .forms import UserRegisterForm, CaptchaForm


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'oauth': UserSocialAuth.objects.filter(user=self.request.user),
        })
        return context


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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user = get_user_model().objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name)
        login(request, user)
        return redirect(reverse('profile'))
