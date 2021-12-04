from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.conf import settings

from django_warrant.utils import get_cognito
from django_warrant.forms import RegisterationForm, ConfirmRegisterationForm, ForgotPasswordForm, ConfirmForgotPasswordForm
from warrant import Cognito
from django.shortcuts import redirect

class RegistrationView(FormView):
    template_name = 'cognito/registration.html'
    form_class = RegisterationForm
    
    def form_valid(self, form):

        cognito_client = Cognito(settings.COGNITO_USER_POOL_ID, settings.COGNITO_APP_ID)
        data = form.cleaned_data
        cognito_client.add_base_attributes(email= data['email'], given_name= data['first_name'], family_name= data['last_name'],)

        cognito_client.register(data['username'], data['password'])

        return redirect('confirm-sign-up-user', username= data['username'])

class ConfirmRegistrationView(FormView):
    template_name = 'cognito/confirm_sign_up.html'
    form_class = ConfirmRegisterationForm
    
    def form_valid(self, form, username=''):

        cognito_client = Cognito(settings.COGNITO_USER_POOL_ID, settings.COGNITO_APP_ID)
        cognito_client.confirm_sign_up(form.cleaned_data['confirmation_code'],username= self.kwargs['username'])

        return redirect('login')

class ForgotPasswordView(FormView):
    template_name = 'cognito/forgot_password.html'
    form_class = ForgotPasswordForm
    
    def form_valid(self, form):

        try:
            cognito_client = Cognito(settings.COGNITO_USER_POOL_ID, settings.COGNITO_APP_ID, username= form.cleaned_data['username'])
            
            cognito_client.initiate_forgot_password()
            return redirect('user-confirm-forgot-password', username= form.cleaned_data['username'])
        except Exception as e:
            raise e

class ConfirmForgotPasswordView(FormView):
    template_name = 'cognito/confirm_forgot_password.html'
    form_class = ConfirmForgotPasswordForm
    
    def form_valid(self, form, username=''):
        try:
            cognito_client = Cognito(settings.COGNITO_USER_POOL_ID, settings.COGNITO_APP_ID, username= self.kwargs['username'])
            data = form.cleaned_data
            cognito_client.confirm_forgot_password(data['confirmation_code'], data['new_password'])

            return redirect('login')
        except Exception as e:
            raise e