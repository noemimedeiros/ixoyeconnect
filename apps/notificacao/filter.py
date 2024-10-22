from django_filters import FilterSet
from django.db import models
from django import forms
from .models import Notificacao
from core.forms import floating_fields
from crispy_forms.layout import Layout, Div, Row, Column, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

class NotificacaoFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

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
        )

    class Meta:
        model = Notificacao
        fields = {
            'data': ['exact', 'lt', 'gt'],
        }