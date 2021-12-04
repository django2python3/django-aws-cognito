from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import ProfileView,UpdateProfileView,MySubsriptions,AdminListUsers,AdminSubscriptions,RegistrationView, ConfirmRegistrationView, ForgotPasswordView, ConfirmForgotPasswordView

urlpatterns = (
    path('', auth_views.login, {'template_name': 'cognito/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'cognito/logout.html'}, name='logout'),
    path('profile/', ProfileView.as_view(),name='profile'),
    path('profile/update/', UpdateProfileView.as_view(),name='update-profile'),
    # path('profile/subscriptions/', MySubsriptions.as_view(),name='subscriptions'),
    path('admin/cognito-users/', AdminListUsers.as_view(),name='admin-cognito-users'),
    path('admin/cognito-users/<username>/', AdminSubscriptions.as_view(),name='admin-cognito-user'),
    
    path('registration/', RegistrationView.as_view(),name='registration-user'),
    path('confirm_sign_up/<str:username>/', ConfirmRegistrationView.as_view(),name='confirm-sign-up-user'),
    path('forgot-password/', ForgotPasswordView.as_view(),name='user-forgot-password'),
    path('forgot-password/<str:username>/', ConfirmForgotPasswordView.as_view(),name='user-confirm-forgot-password'),
)