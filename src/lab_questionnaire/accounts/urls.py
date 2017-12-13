from django.urls import path
from .views import RegisterView, RegisterCompleteView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_done, \
    password_reset_complete
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path(r'login/', login,
         {"template_name": "accounts/login.html"},
         name='login'),

    path(r'logout/', logout,
         {"template_name": "accounts/logout.html"},
         name='logout'),

    path(r'password-change/', password_change,
         {"template_name": "accounts/password_change.html"},
         name='password_change'),

    path(r'password-change-done/', password_change_done,
         {"template_name": "password_change_done.html"},
         name='password_change_done'),

    path(r'register/', RegisterView.as_view(),
         name='register'),

    path(r'register/done', TemplateView.as_view(
        template_name="accounts/register_done.html"),
         name='register_done'),

    path(r'register/complete/<slug:uidb64>/<slug:token>', RegisterCompleteView.as_view(),
         name='register_complete'),

    path(r'password-reset/', PasswordResetView.as_view(),
         name='password_reset'),

    path(r'password-reset/done/', password_reset_done,
         {"template_name": "accounts/password_reset_done.html"},
         name='password_reset_done'),

    path(r'password-reset/confirm/<slug:uidb64>/<slug:token>', password_reset_confirm,
         {"template_name": "accounts/password_reset_confirm.html"},
         name='password_reset_confirm'),

    path(r'password-reset/complete/', password_reset_complete,
         {"template_name": "accounts/password_reset_complete.html"},
         name='password_reset_complete'),
]
