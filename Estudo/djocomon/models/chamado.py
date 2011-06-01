from django.db import models

# Create your models here.
from django.utils.datetime_safe import datetime
from djocomon.models.secao import Secao

class Chamado(models.Model):
    numero = models.BigIntegerField(blank=True, null=True)
    data_hora_criacao_chamado = models.DateTimeField(blank=True, default=datetime.now, null=True)
    atualizado_em = models.DateTimeField(blank=True, auto_now=True, default=datetime.now ,null=True)

    secao = Secao()


