from django_filters import FilterSet, CharFilter
from django.db import models
from .models import Escala
from core.forms import floating_fields

class EscalaFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

    class Meta:
        model = Escala
        fields = ('funcao_membro', )
        filter_overrides = {
            models.CharField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                }
            },
        }