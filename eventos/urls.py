# eventos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. Listagem (Página Inicial)
    path('', views.lista_eventos, name='lista_eventos'), 
    
    # 2. Detalhe do Evento
    path('evento/<int:pk>/', views.detalhe_evento, name='detalhe_evento'), 
    
    path('comprar/<int:ingresso_pk>/', views.comprar_ingresso, name='comprar_ingresso'),
]
