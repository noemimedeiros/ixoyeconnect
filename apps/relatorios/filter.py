from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import AtividadesCulto, RelatorioCulto
from core.forms import floating_fields
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import Layout, Div, Row, Column, HTML

class RelatorioCultoFilter(FilterSet):
    atividades = ModelMultipleChoiceFilter(queryset=AtividadesCulto.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

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
                FloatingField('ministro', css_class='form-primary'),
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