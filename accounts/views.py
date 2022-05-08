from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from accounts.forms import RegisterForm, LoginForm


class MySignupView(CreateView):
    form_class = RegisterForm
    success_url = '/login/'
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Регистрация'
        return context


class MyLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Вход'
        return context
