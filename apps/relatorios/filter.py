from django import forms
from django.db.models import Q
from django_filters import FilterSet, ModelMultipleChoiceFilter, ModelChoiceFilter, CharFilter, BooleanFilter

from usuario.models import Membro
from .models import AtividadesCulto, RelatorioCulto
from core.forms import floating_fields
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_bootstrap5.bootstrap5 import FloatingField, Switch
from crispy_forms.layout import Layout, Div, Row, Column, HTML

class RelatorioCultoFilter(FilterSet):
    atividades = ModelMultipleChoiceFilter(queryset=AtividadesCulto.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    ministro = ModelChoiceFilter(queryset=Membro.objects.none(), required=False, to_field_name='nome')
    ministro_texto = CharFilter(required=False, label='Ministro')
    ministro_externo = BooleanFilter(widget=forms.CheckboxInput, required=False, label='Ministro de fora? (Digitar nome)', method='filter_ministro_externo')
    selecionar_todas_atividades = BooleanFilter(widget=forms.CheckboxInput, required=False, label='Selecionar todas atividades', method='filter_selecionar_todas_atividades')
    
    def filter_ministro_externo(self, queryset, name, value):
        if value:
            return queryset.filter(ministro__nome__icontains=value)
        return queryset
    
    def filter_selecionar_todas_atividades(self, queryset, name, value):
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

        self.form.fields['data'].label = 'Data exata'
        instituicao = self.queryset[0].instituicao
        if instituicao:
            membros = Membro.objects.filter(
                Q(sede_id=instituicao.pk) & (Q(admin=True) |
                Q(funcoes__funcao__funcao__icontains='pastor') |
                Q(funcoes__funcao__funcao__icontains='ministro') |
                Q(funcoes__funcao__funcao__icontains='pregador'))
            )

            self.form.fields['ministro'].queryset = membros

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
                )
            ),
            Div(
                HTML('<h6 class="mb-3">Informações:</h6>'),
                Div(
                    Switch('ministro_externo'),
                    FloatingField('ministro', css_class='form-primary'),
                    FloatingField('ministro_texto', css_class='form-primary'),
                ),
                HTML('<h6 class="mb-3">Culto ou Evento:</h6>'),
                Row(
                    Column(
                        FloatingField('culto', css_class='form-primary'),
                    ),
                    Column(
                        FloatingField('evento', css_class='form-primary'),
                    )
                )
            ),
            Switch('selecionar_todas_atividades'),
            InlineCheckboxes('atividades', css_class='atividades-checkboxes')
        )

    class Meta:
        model = RelatorioCulto
        fields = {
            'data': ['exact', 'lt', 'gt'],
            'evento': ['exact'],
            'culto': ['exact'],
            'ministro': ['exact'],
            'atividades': ['exact']
        }