# eventos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento # Certifique-se de importar seus modelos
from .forms import EventoForm, IngressoFormSet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# 1. View de Listagem
def lista_eventos(request):
    eventos = Evento.objects.all().order_by('data_evento')
    context = {
        'eventos': eventos
    }
    # ATENÇÃO: O caminho DEVE ser 'eventos/lista_eventos.html'
    return render(request, 'eventos/lista_eventos.html', context)

# 2. View de Detalhe
def detalhe_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk) 
    context = {
        'evento': evento
    }
    return render(request, 'eventos/detalhe_evento.html', context)

