from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.conf import settings

from django_warrant.utils import get_cognito
from django_warrant.forms import ProfileForm


class TokenMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):

        if not request.session.get('REFRESH_TOKEN'):
            print('Got Here')
            return self.handle_no_permission()
        return super(TokenMixin, self).dispatch(
            request, *args, **kwargs)

class GetUserMixin(object):

    def get_user(self):

        c = get_cognito(self.request)
        return c.get_user(attr_map=settings.COGNITO_ATTR_MAPPING)

class ProfileView(LoginRequiredMixin,TokenMixin,GetUserMixin,TemplateView):
    template_name = 'cognito/profile.html'

    def get_context_data(self, **kwargs):

        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        return context


class UpdateProfileView(LoginRequiredMixin,TokenMixin,GetUserMixin,FormView):
    template_name = 'cognito/update-profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('update-profile')

    def get_initial(self):
        u = self.get_user()
        return u.__dict__
    
    def form_valid(self, form):
        cognito_client = get_cognito(self.request)
        cognito_client.update_profile(form.cleaned_data,settings.COGNITO_ATTR_MAPPING)
        messages.success(self.request,'You have successfully updated your profile.')
        return super(UpdateProfileView, self).form_valid(form)
