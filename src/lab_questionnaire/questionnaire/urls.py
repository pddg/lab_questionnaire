from django.urls import path
from .views import TopPageView, EditProfileView
from django.views.generic import CreateView
from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('', TopPageView.as_view(),
         name='top_page'),

    path(r'profile/', EditProfileView.as_view(),
         name='edit_profile'),
]
