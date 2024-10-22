from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from django.db import models
from django import forms
from .models import Funcao, Membro
from core.forms import floating_fields
from crispy_forms.layout import Layout, Div, HTML, Row, Column, MultiField
from crispy_bootstrap5.bootstrap5 import FloatingField, Switch

class MembroFilter(FilterSet):
    com_cargos = BooleanFilter(widget=forms.CheckboxInput, label='Membros com Cargos/Funções', method='filter_com_cargos')
    sem_cargos = BooleanFilter(widget=forms.CheckboxInput, label='Membros sem Cargos/Funções', method='filter_sem_cargos')
    por_cargos = ModelChoiceFilter(widget=forms.Select, label='Por Cargo/Função', queryset=Funcao.objects.all(), method='filter_por_funcao')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

        self.form.fields['data_nascimento__year'].label = 'Ano exato'
        self.form.fields['ano_ingressao'].label = 'Ano exato'

        self.form.fields['data_nascimento__year__gt'].label = 'Ano maior que'
        self.form.fields['data_nascimento__year__lt'].label = 'Ano menor que'
        self.form.fields['ano_ingressao__gt'].label = 'Ano maior que'
        self.form.fields['ano_ingressao__lt'].label = 'Ano menor que'

        self.form.helper.layout = Layout(
            Div(
                HTML('<h6 class="mb-3">Ano de Nascimento:</h6>'),
                FloatingField('data_nascimento__year', css_class='form-primary'),
                Row(
                    Column(
                        FloatingField('data_nascimento__year__gt', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('data_nascimento__year__lt', css_class='form-primary')
                    )
                )
            ),
            Div(
                HTML('<h6 class="mb-3">Ano de Ingressão:</h6>'),
                FloatingField('ano_ingressao', css_class='form-primary'),
                Row(
                    Column(
                        FloatingField('ano_ingressao__gt', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('ano_ingressao__lt', css_class='form-primary')
                    ),
                )
            ),
            Div(
                HTML('<h6 class="mb-3">Cargos/Funções:</h6>'),
                FloatingField('por_cargos', css_class='form-primary'),
                Switch('com_cargos'),
                Switch('sem_cargos'),
            )
        )

    class Meta:
        model = Membro
        fields = {
            'ano_ingressao': ['exact', 'lt', 'gt'],
            'data_nascimento': ['year__exact', 'year__lt', 'year__gt']
        }

    def filter_com_cargos(self, queryset, name, value):
        if value:
            try:
                return queryset.filter(funcoes__membro_id=self.request.user.pk).distinct()
            except AttributeError:
                return queryset.filter(funcoes__isnull=False).distinct()
        return queryset
    
    def filter_por_funcao(self, queryset, name, value):
        return queryset.filter(funcoes__funcao=value).distinct()
    
    def filter_sem_cargos(self, queryset, name, value):
        return queryset.filter(funcoes__isnull=True).distinct()