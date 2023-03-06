from django.shortcuts import render
from django.views.generic import ListView
from .models import *


# Create your views here.
class Home(ListView):
    model = Flats
    paginate_by = 5 
    template_name = "flats_publ/home.html"
    context_object_name = "flats"
    