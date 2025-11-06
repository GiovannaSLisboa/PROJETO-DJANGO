# eventos/urls.py
from accounts.views import AccountsLoginView
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.lista_eventos, name='lista_eventos'), 
    path('accounts/login/', AccountsLoginView.as_view(), name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('evento/<int:pk>/', views.detalhe_evento, name='detalhe_evento'), 
    path('admin/login/', AccountsLoginView.as_view(), name="admin_login"),
    path('comprar/<int:ingresso_pk>/', views.comprar_ingresso, name='comprar_ingresso'),
]
