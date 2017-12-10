from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class TopPageView(TemplateView):
    template_name = "top_page.html"
