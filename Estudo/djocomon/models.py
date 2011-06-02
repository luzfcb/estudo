# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models

# Create your models_old here.
from django.utils.datetime_safe import datetime


class Situacao(models.Model):
    status = models.CharField(max_length=255)
    class Meta:
        verbose_name = _(u'Situação')
        verbose_name_plural = _(u'Situações')

class Secao(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        verbose_name = _(u'Seção')
        verbose_name_plural = _(u'Seções')



class Ocorrencia(models.Model):
    numero = models.CharField(max_length=18,blank=False, null=False)
    data_hora_criacao_ocorrencia = models.DateTimeField(blank=True, default=datetime.now, null=True)
    atualizado_em = models.DateTimeField(auto_now=True, null=True, auto_now_add=True)
    
    secao = models.ForeignKey(Secao)
    operador = models.ForeignKey(User)
    situacao = models.ForeignKey(Situacao)

    class Meta:
        verbose_name = _(u'Ocorrência')
        verbose_name_plural = _(u'Ocorrências')
    
 #   def __init__(self):


  