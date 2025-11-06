# eventos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento, Ingresso, Compra, Local, Categoria
from .forms import EventoForm, IngressoFormSet
from django.db import transaction
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

@login_required
def comprar_ingresso(request, ingresso_pk):
    # Obtém o tipo de ingresso específico que o usuário quer comprar
    ingresso = get_object_or_404(Ingresso, pk=ingresso_pk)
    
    if request.method == 'POST':
        try:
            # Pega a quantidade do formulário (que vem do input 'quantidade' no detalhe_evento.html)
            quantidade = int(request.POST.get('quantidade', 0))
        except ValueError:
            messages.error(request, 'Quantidade inválida.')
            return redirect('detalhe_evento', pk=ingresso.evento.pk)

        if quantidade <= 0:
            messages.error(request, 'A quantidade deve ser maior que zero.')
            return redirect('detalhe_evento', pk=ingresso.evento.pk)

        # Inicia uma transação atômica para garantir que a compra e o estoque sejam atualizados juntos
        try:
            with transaction.atomic():
                # 1. Trava e verifica o estoque (SELECT FOR UPDATE)
                ingresso_para_atualizar = Ingresso.objects.select_for_update().get(pk=ingresso_pk)
                
                if ingresso_para_atualizar.quantidade_disponivel < quantidade:
                    messages.error(request, 'Estoque insuficiente para a quantidade solicitada.')
                    return redirect('detalhe_evento', pk=ingresso.evento.pk)

                # 2. Registra a Compra (Cria o objeto Compra que aparece no Admin)
                preco_unitario = ingresso_para_atualizar.preco
                valor_total = preco_unitario * quantidade

                Compra.objects.create(
                    usuario=request.user,
                    ingresso=ingresso_para_atualizar,
                    quantidade=quantidade,
                    valor_total=valor_total,
                    status='paga' # Assumindo pagamento concluído
                )

                # 3. Atualiza o Estoque e Salva
                ingresso_para_atualizar.quantidade_disponivel -= quantidade
                ingresso_para_atualizar.save()

                messages.success(request, f'Compra de {quantidade}x {ingresso.tipo.capitalize()} concluída! Total: R${valor_total:.2f}')
                return redirect('detalhe_evento', pk=ingresso.evento.pk)
        
        except Exception as e:
            messages.error(request, f'Erro interno ao processar a compra. Tente novamente.')
            # Em produção, você registraria o erro (e)
            return redirect('detalhe_evento', pk=ingresso.evento.pk)
    
    # Se for uma requisição GET, apenas redireciona
    return redirect('detalhe_evento', pk=ingresso.evento.pk)