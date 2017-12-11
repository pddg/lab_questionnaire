from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, ListView, FormView
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import get_template
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import StudyOffice


class TopPageView(ListView):
    template_name = "top_page.html"
    model = StudyOffice


class EditProfileView(UpdateView):
    template_name = "edit_profile.html"
    fields = ("first_choice",)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('top_page')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditProfileView, self).dispatch(*args, **kwargs)


class RegistView(FormView):
    pass
