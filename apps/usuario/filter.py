from django_filters import FilterSet, TimeFilter
from django.db import models
from django import forms
from .models import Membro
from core.forms import floating_fields
from crispy_forms.layout import Layout, Div, HTML, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField, Switch

class MembroFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

        self.form.helper.layout = Layout(
            Div(
                HTML('<h6 class="mb-3">Ano de Nascimento:</h6>'),
                FloatingField('data_nascimento__year', css_class='form-primary'),
                Row(
                    Column(
                        FloatingField('data_nascimento__year__lt', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('data_nascimento__year__gt', css_class='form-primary')
                    )
                )
            ),
            Div(
                HTML('<h6 class="mb-3">Ano de Ingressão:</h6>'),
                FloatingField('ano_ingressao', css_class='form-primary datepicker'),
                Row(
                    Column(
                        FloatingField('ano_ingressao__lt', css_class='form-primary datepicker')
                    ),
                    Column(
                        FloatingField('ano_ingressao__gt', css_class='form-primary datepicker')
                    )
                )
            )
        )

    class Meta:
        model = Membro
        fields = {
            'ano_ingressao': ['exact', 'lt', 'gt'],
            'data_nascimento': ['year__lt', 'year__gt']
        }