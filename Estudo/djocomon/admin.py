from django.contrib import admin

from djocomon.models.secao import Secao
from djocomon.models.chamado import Chamado


admin.site.register(Chamado)
admin.site.register(Secao)