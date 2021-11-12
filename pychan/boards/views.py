from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from pychan.mixins import ChanCoreView
from .models import Board, Post

class ThreadView(ChanCoreView, ListView):
    model = Post
    template_name = "thread.html"

    def get_queryset(self):
        return Post.objects.filter(
            Q(thread__id=self.kwargs['pk']) |
            Q(pk=self.kwargs['pk'])
        ).order_by('timestamp')

class BoardView(ChanCoreView, ListView):
    model = Board
    template_name = "board.html"

    def get_queryset(self):
        return Post.objects.filter(board__short=self.kwargs['short'], thread=None).order_by('-timestamp')

class ThreadCreateView(CreateView):
    model = Post
    template_name = "objCreateUpdate.html"
    fields = ['image', 'message']

    def form_valid(self, form):
        board = Board.objects.get(short=self.kwargs['short'])
        form.instance.board = board
        return super(ThreadCreateView, self).form_valid(form)

class PostCreateView(CreateView):
    model = Post
    template_name = "objCreateUpdate.html"
    fields = ['image', 'message']

    def form_valid(self, form):
        thread = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.thread = thread
        return super(PostCreateView, self).form_valid(form)

class BoardEditMixin(object):
    def get_success_url(self):
        return reverse('boardList')

class BoardListView(ListView):
    model = Board
    template_name = "boards.html"

    def get_queryset(self):
        return Board.objects.all()

class BoardCreateView(BoardEditMixin, CreateView):
    model = Board
    template_name = "objCreateUpdate.html"
    fields = '__all__' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_name"] = "Board" 
        return context

class BoardUpdateView(BoardEditMixin, UpdateView):
    model = Board
    template_name = "objCreateUpdate.html"
    fields = '__all__' 

class BoardDeleteView(BoardEditMixin, DeleteView):
    model = Board
    fields = '__all__' 
