from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.forms import Form
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from social_django.models import UserSocialAuth

from .decorators import logout_required
from .forms import RegisterForm


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'oauth': UserSocialAuth.objects.filter(user=self.request.user),
        })
        return context


@method_decorator(logout_required, name='dispatch')
class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        user = get_user_model().objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
        login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
        return super(RegisterView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class UnregisterView(FormView):
    template_name = 'accounts/unregister.html'
    form_class = Form
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.request.user.is_active = False
        self.request.user.save()
        return super(UnregisterView, self).form_valid(form)
