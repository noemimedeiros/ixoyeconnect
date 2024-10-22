from django import forms
from agenda.models import AgendaSemanal
from usuario.models import InstituicaoSede, Membro
from core.forms import FormBaseIxoye
from relatorios.models import AtividadesCulto, RelatorioCulto
from crispy_forms.layout import Layout, Div, HTML, Row, Column, Submit, Hidden
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_bootstrap5.bootstrap5 import FloatingField

class RelatorioCultoForm(FormBaseIxoye):
    atividades = forms.ModelMultipleChoiceField(queryset=AtividadesCulto.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)

    class Meta:
        model = RelatorioCulto
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput(),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time'})
        }

    def clean(self):
        cleaned_data = super().clean()
        total_pessoas = cleaned_data.get('total_pessoas', 0)
        total_mulheres = cleaned_data.get('total_mulheres', 0)
        total_homens = cleaned_data.get('total_homens', 0)
        total_visitantes = cleaned_data.get('total_visitantes', 0)

        return cleaned_data

    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)

        if instituicao:
            self.fields['instituicao'].queryset = InstituicaoSede.objects.filter(pk=instituicao.pk)
            self.fields['instituicao'].initial = instituicao

            self.fields['ministro'].queryset = Membro.objects.filter(sede_id=instituicao.pk, admin=True)
            self.fields['culto'].queryset = AgendaSemanal.objects.filter(instituicao_id=instituicao.pk)

        self.helper.layout = Layout(
            Hidden('instituicao', value=instituicao.pk),
            Div(
                HTML('<h6 class="mb-3">Informações:</h6>'),
                Row(
                    Column(
                        FloatingField('data', css_class='form-primary datepicker')
                    ),
                    Column(
                        FloatingField('hora_inicio', css_class='form-primary datepicker')
                    ),
                    Column(
                        FloatingField('hora_termino', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('ministro', css_class='form-primary')
                    )
                )
            ),
            Div(
                HTML('<h6 class="mb-3">Total de participantes:</h6>'),
                Row(
                    Column(
                        FloatingField('total_pessoas', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('total_mulheres', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('total_homens', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('total_jovens', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('total_juniores', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('total_visitantes', css_class='form-primary')
                    )
                )
            ),
            Div(
                HTML('<h6 class="mb-3">Programação do Dia ou Evento:</h6>'),
                Row(
                    Column(
                        FloatingField('culto', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('evento', css_class='form-primary')
                    )
                )
            ),
            Div(
                HTML('<h6 class="mb-3">Dízimos e Ofertas:</h6>'),
                Row(
                    Column(
                        FloatingField('total_dizimos', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('total_ofertas', css_class='form-primary')
                    )
                )
            ),
            Div(
                HTML('<h6 class="mb-3">Eventos Especiais:</h6>'),
                Row(
                    Column(
                        FloatingField('total_novos_convertidos', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('total_novos_batizandos', css_class='form-primary')
                    )
                )
            ),
            InlineCheckboxes('atividades', css_class='atividades-checkboxes'),
        )