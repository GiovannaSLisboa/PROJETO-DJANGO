from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_evento = models.DateTimeField()
    local = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='eventos/', null=True, blank=True)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Ingresso(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='ingressos')
    tipo = models.CharField(max_length=50, choices=[
        ('inteira', 'Inteira'),
        ('meia', 'Meia entrada'),
        ('vip', 'VIP'),
    ])
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade_disponivel = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tipo} - {self.evento.titulo}"


class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ingresso = models.ForeignKey(Ingresso, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    data_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} comprou {self.quantidade} de {self.ingresso.tipo}"