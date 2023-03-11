from django.shortcuts import render
from django.views.generic import ListView
from .models import *


# Create your views here.
class Home(ListView):
    model = Flats
    paginate_by = 5 
    template_name = "flats_publ/home.html"
    context_object_name = "flats"
    
    
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['sityes'] = set([s.sity for s in Flats.objects.all()])
        
        return context
    
    
