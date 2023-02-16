from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView

class MainView(TemplateView):

    template_name = "main/index.html"


class GalaryView(TemplateView):

    template_name = "main/gal.html"
