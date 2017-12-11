from django.views.generic import TemplateView, UpdateView, ListView, FormView, CreateView
from django.utils.decorators import method_decorator
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
