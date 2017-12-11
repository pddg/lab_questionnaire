from django.urls import path
from .views import TopPageView, EditProfileView, RegistView
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('', TopPageView.as_view(), name='top_page'),
    path(r'profile/', EditProfileView.as_view(), name='edit_profile'),
    path(r'login/', login, {"template_name": "login.html"}, name='login'),
    path(r'logout/', logout, {"template_name": "logout.html"}, name='logout'),
    path(r'regist/', RegistView.as_view(), name='regist'),
]
