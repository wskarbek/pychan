from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateWalletView.as_view(), name='createWalletView'),
    path('send/', views.SendView.as_view(), name='sendView'),
]