import os
from django import template

register = template.Library()

@register.filter
def get_tipo_display(tipo):
    tipos_contriuicao = {
        'oferta': 'Oferta',
        'dizimo': 'Dízimo',
        'doacao': 'Doação',
        'caridade': 'Campanhas de Caridade',
        'missoes': 'Contribuição para Missões',
        'manutencao_tempo': 'Manutenção do Templo'
    }
    return tipos_contriuicao[tipo]