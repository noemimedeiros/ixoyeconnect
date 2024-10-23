from django_filters import FilterSet, BooleanFilter
from django.db.models import Q
from django import forms
from .models import Evento
from core.forms import floating_fields
from crispy_forms.layout import Fieldset, Div, Layout, HTML, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField, Switch

class EventoFilter(FilterSet):
    gratuito = BooleanFilter(widget=forms.CheckboxInput, label='Gratuito', method='filter_gratuito')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

        self.form.helper.disable_csrf = True

        self.form.helper.layout = Layout(
            Div(
                HTML('<h6 class="mb-3">Data:</h6>'),
                FloatingField('data', css_class='form-primary datepicker'),
                Row(
                    Column(
                        FloatingField('data__gt', css_class='form-primary datepicker')
                    ),
                    Column(
                        FloatingField('data__lt', css_class='form-primary datepicker')
                    )
                ),
            ),
            Div(
                HTML('<h6 class="mb-3">Valor:</h6>'),
                Row(
                    Column(
                        FloatingField('valor__gt', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('valor__lt', css_class='form-primary')
                    )
                ),
                Switch('gratuito'),
            )
        )

    class Meta:
        model = Evento
        fields = {
            'valor': ['lt', 'gt'],
            'data': ['exact', 'lt', 'gt'],
        }

    def filter_gratuito(self, queryset, name, value):
        return queryset.filter(Q(valor__isnull=True) | Q(valor=0))