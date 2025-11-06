

from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.lista_eventos, name='lista_eventos'), 
    
    
    path('evento/<int:pk>/', views.detalhe_evento, name='detalhe_evento'), 
    
    path('comprar/<int:ingresso_pk>/', views.comprar_ingresso, name='comprar_ingresso'),
]
