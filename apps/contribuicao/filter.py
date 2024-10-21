from django_filters import FilterSet, TimeFilter
from django.db import models
from django import forms
from .models import Contribuicao
from core.forms import floating_fields

class ContribuicaoFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

    class Meta:
        model = Contribuicao
        fields = ('metodo', 'tipo', 'departamento', )