from django_filters import FilterSet, TimeFilter
from django.db import models
from django import forms
from .models import AgendaSemanal
from core.forms import floating_fields

class AgendaSemanalFilter(FilterSet):
    hora = TimeFilter(
        field_name='hora', 
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)
        self.form.helper.disable_csrf = True

    class Meta:
        model = AgendaSemanal
        fields = ('dia_semana', 'hora', )