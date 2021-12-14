from django.urls import path

from . import views

urlpatterns = [
    path('op/', views.BoardListView.as_view(), name='boardList'),
    path('op/add', views.BoardCreateView.as_view(), name='boardCreate'),
    path('op/update/<pk>', views.BoardUpdateView.as_view(), name='boardUpdate'),
    path('op/delete/<pk>', views.BoardDeleteView.as_view(), name='boardDelete'),
    path('<str:short>/add', views.ThreadCreateView.as_view(), name='threadCreate'),
    path('<str:short>/<int:pk>/add', views.PostCreateView.as_view(), name='postCreate'),
    path('<str:short>/', views.BoardView.as_view(), name='boardView'),
    path('<str:short>/<int:pk>/', views.ThreadView.as_view(), name='thread'),
]