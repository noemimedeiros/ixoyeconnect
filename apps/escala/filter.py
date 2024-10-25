from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from django.db import models

from usuario.models import FuncaoMembro
from .models import Escala
from core.forms import floating_fields
from crispy_forms.layout import Div, Layout, HTML, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField

class EscalaFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)
        self.form.helper.disable_csrf = True

        self.form.fields['funcao_membro__funcao'].label = 'Cargo'
        self.form.fields['funcao_membro__departamento'].label = 'Departamento'

        self.form.helper.layout = Layout(
            Div(
                HTML('<h6 class="mb-3">Função e Departamento:</h6>'),
                FloatingField('funcao_membro__funcao', css_class='form-primary'),
                FloatingField('funcao_membro__departamento', css_class='form-primary'),
            ),
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
                HTML('<h6 class="mb-3">Hora:</h6>'),
                FloatingField('hora', css_class='form-primary'),
                Row(
                    Column(
                        FloatingField('hora__gt', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('hora__lt', css_class='form-primary')
                    )
                ),
            ),
        )

    class Meta:
        model = Escala
        fields = {
            'funcao_membro__funcao': ['exact'],
            'funcao_membro__departamento': ['exact'],
            'data': ['lt', 'gt', 'exact'],
            'hora': ['exact', 'lt', 'gt']
        }