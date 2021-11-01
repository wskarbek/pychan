from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Board, Post

class ThreadView(ListView):
    model = Post
    template_name = "thread.html"

    def get_query_set(self):
        return Post.objects.filter(thread__id=self.kwargs['pk'].order_by('timestamp'))

class BoardView(ListView):
    model = Post
    template_name = "board.html"

    def get_queryset(self):
        return Post.objects.filter(board__short=self.kwargs['short'], thread=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board_name"] = Board.objects.get(short=self.kwargs['short'])
        return context

class BoardListView(ListView):
    model = Board
    template_name = "boards.html"

    def get_queryset(self):
        return Board.objects.all()

class BoardCreateView(CreateView):
    model = Board
    template_name = "objCreateUpdate.html"
    fields = ['name', 'short', 'max_threads', 'nsfw']
    success_url = '/boards'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_name"] = "Board" 
        return context

class BoardUpdateView(UpdateView):
    model = Board
    template_name = "objCreateUpdate.html"
    fields = ['name', 'short', 'max_threads', 'nsfw']
    success_url = '/boards'

class BoardDeleteView(DeleteView):
    model = Board
    fields = ['name', 'short', 'max_threads', 'nsfw']
    success_url = '/boards'