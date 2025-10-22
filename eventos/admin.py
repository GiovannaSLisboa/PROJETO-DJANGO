from django.contrib import admin
from .models import Categoria, Local, Evento, Ingresso, Compra


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'capacidade', 'endereco')
    search_fields = ('nome', 'endereco')


class IngressoInline(admin.TabularInline):
    model = Ingresso
    extra = 1
    fields = ('tipo', 'preco', 'quantidade_disponivel')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'local', 'categoria', 'data_evento', 'preco_base', 'organizador')
    list_filter = ('categoria', 'local', 'data_evento')
    search_fields = ('titulo', 'descricao')
    inlines = [IngressoInline]


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'ingresso', 'quantidade', 'valor_total', 'status', 'data_compra')
    list_filter = ('status', 'data_compra')
    search_fields = ('usuario__username', 'ingresso__evento__titulo')
    readonly_fields = ('data_compra', 'valor_total')
