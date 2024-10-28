from django import template

register = template.Library()

@register.filter
def get_atividade(relatorio, atividade):
    if relatorio.atividades.filter(atividade=atividade).exists():
        return '<i class="fa-solid fa-check text-success"></i>'
    else:
        return '<i class="fa-solid fa-xmark text-danger"></i>'
    
@register.filter
def culto_com_escalas(culto, escalas):
    datas_escalas = escalas.values_list('data', flat=True)
    return (culto.data in datas_escalas)