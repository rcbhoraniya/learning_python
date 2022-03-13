from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import *
from django.contrib.auth.forms import *
from .forms import *
# Create your views here.
from django.views.generic import CreateView

class PermissionDeniedView(TemplateView):
    template_name = 'authentication/permission_denied.html'


# class UserAccessMixin(PermissionRequiredMixin, LoginRequiredMixin):
    # login_url = 'authentication:login'
    # permission_denied_message = 'No permission'
    # raise_exception = False
    # redirect_field_name = 'next'

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
    #     if not self.has_permission():
    #         return redirect('authentication:permissiondenied')
    #     return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'authentication/registration.html'
    success_url = reverse_lazy('authentication:login')


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'authentication/login.html'
    next_page = 'inventory:home'
    # redirect_field_name = 'stocks:index'


class UserLogoutView(LogoutView):
    # template_name = 'stocks/logout.html'
    next_page = 'authentication:login'