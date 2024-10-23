from django import forms
from django.db.models import Q
from django_filters import FilterSet, ChoiceFilter

from .models import RelatorioCulto
from core.forms import floating_fields
from crispy_forms.bootstrap import InlineRadios
from crispy_bootstrap5.bootstrap5 import FloatingField, Switch
from crispy_forms.layout import Layout, Div, Row, Column, HTML

class RelatorioCultoFilter(FilterSet):
    EVENTOS_OU_CULTOS = (
        ('apenas_cultos', 'Apenas Cultos'),
        ('apenas_eventos', 'Apenas Eventos')
    )

    apenas_eventos_ou_cultos = ChoiceFilter(choices=EVENTOS_OU_CULTOS, empty_label='Todos', widget=forms.RadioSelect(), method='filter_apenas_eventos_ou_cultos', label='', required=False)

    def filter_apenas_eventos_ou_cultos(self, queryset, name, value):
        if value == 'apenas_cultos':
            return queryset.filter(evento__isnull=False, culto__isnull=True)
        return queryset.filter(evento__isnull=True, culto__isnull=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

        self.form.fields['data'].label = 'Data exata'
        self.form.fields['data__year'].label = 'Ano'
        self.form.fields['data__year__gt'].label = 'Ano inicial'
        self.form.fields['data__year__lt'].label = 'Ano final'

        self.form.helper.layout = Layout(
            Div(
                HTML('<h6 class="mb-3">Data ou Período:</h6>'),
                FloatingField('data', css_class='form-primary datepicker'),
                Row(
                    Column(
                        FloatingField('data__gt', css_class='form-primary datepicker')
                    ),
                    Column(
                        FloatingField('data__lt', css_class='form-primary datepicker')
                    )
                ),
                HTML('<h6 class="mb-3">Ano ou Período por ano:</h6>'),
                FloatingField('data__year', css_class='form-primary'),
                Row(
                    Column(
                        FloatingField('data__year__gt', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('data__year__lt', css_class='form-primary')
                    )
                ),
            ),
            Div(
                HTML('<h6 class="mb-3">Filtrar relatório:</h6>'),
                InlineRadios('apenas_eventos_ou_cultos')
            )
        )

    class Meta:
        model = RelatorioCulto
        fields = {
            'data': ['exact', 'lt', 'gt', 'year__exact', 'year__lt', 'year__gt'],
        }