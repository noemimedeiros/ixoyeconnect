from django import template

register = template.Library()

@register.filter
def icone_notificacao(self):
    if self == 'Post':
        return 'fa-book'
    if self == 'Escala':
        return 'fa-clipboard-list'
    if self == 'Evento':
        return 'fa-calendar-day'