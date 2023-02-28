from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView

class MainView(TemplateView):

    template_name = "main/index.html"


class GalaryNsuemView(TemplateView):

    template_name = "main/nsuem_gal.html"

class BaseOrderView(TemplateView):

    template_name = "main/base_gal.html"

class AuthorityOrderView(TemplateView):

    template_name = "main/orders_gal.html"
