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

# 3. View de Criação (para o formulário)
@login_required 
def criar_evento(request):
    
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES) 
        
        if form.is_valid():
            
            # 1. Salva o Evento principal sem commitar (para preencher o organizador)
            evento = form.save(commit=False)
            evento.organizador = request.user
            
            # 2. Instancia o Formset, ligando-o à instância do Evento
            formset = IngressoFormSet(request.POST, request.FILES, instance=evento)
            
            if formset.is_valid():
                
                # 3. Salva o Evento principal no banco
                evento.save() 
                
                # 4. Salva todos os Ingressos associados
                formset.save() 
                
                messages.success(request, '🎉 O evento e seus ingressos foram criados com sucesso!')
                return redirect('lista_eventos')
    else:
        # Lógica GET: Instancia ambos os formulários
        form = EventoForm() 
        # Cria um formset vazio, ligado a uma instância vazia de Evento
        formset = IngressoFormSet(instance=Evento()) 
        
    context = {
        'form': form,
        'formset': formset, # <--- Passa o formset para o template
        'titulo_pagina': 'Criar Novo Evento'
    }
    return render(request, 'eventos/criar_evento.html', context)