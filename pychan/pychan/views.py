from django.views.generic import ListView
from boards.models import Board

class IndexView(ListView):
    model = Board
    template_name = "pychan/index.html"
    
