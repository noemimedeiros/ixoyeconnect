from django import forms
from django.db.models import Q
from agenda.models import AgendaSemanal
from usuario.models import InstituicaoSede, Membro
from core.forms import FormBaseIxoye
from relatorios.models import AtividadesCulto, RelatorioCulto
from crispy_forms.layout import Layout, Div, HTML, Row, Column, Submit, Hidden
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_bootstrap5.bootstrap5 import FloatingField, Switch

class RelatorioCultoForm(FormBaseIxoye):
    atividades = forms.ModelMultipleChoiceField(queryset=AtividadesCulto.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    ministro = forms.ModelChoiceField(queryset=Membro.objects.none(), required=False, to_field_name='nome')
    ministro_texto = forms.CharField(required=False, label='Ministro')
    ministro_externo = forms.BooleanField(required=False, label='Ministro de fora? (Digitar nome)')

    class Meta:
        model = RelatorioCulto
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput(),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time'}),
            'total_dizimos': forms.TextInput(),
            'total_ofertas': forms.TextInput()
        }

    def clean_ministro(self):
        data = self.cleaned_data['ministro']
        if self.data.get('ministro_externo') == 'on':
            data = self.data.get('ministro_texto')
        return data

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

            membros = Membro.objects.filter(
                Q(sede_id=instituicao.pk) & (Q(admin=True) |
                Q(funcoes__funcao__funcao__icontains='pastor') |
                Q(funcoes__funcao__funcao__icontains='ministro') |
                Q(funcoes__funcao__funcao__icontains='pregador'))
            )

            self.fields['ministro'].queryset = membros
            self.fields['culto'].queryset = AgendaSemanal.objects.filter(instituicao_id=instituicao.pk)

        self.fields['total_dizimos'].localize = True
        self.fields['total_ofertas'].localize = True

        if self.instance.pk:
            if self.instance.ministro not in membros.values_list('nome', flat=True):
                self.fields['ministro_externo'].initial = True
                self.fields['ministro_texto'].initial = self.instance.ministro
            else:
                self.fields['ministro'].initial = self.instance.ministro

        self.helper.layout = Layout(
            Hidden('instituicao', value=instituicao.pk),
            Div(
                HTML('<h6 class="mb-3">Informações:</h6>'),
                Row(
                    Column(
                        FloatingField('data', css_class='form-primary datepicker')
                    ),
                    Column(
                        FloatingField('hora_inicio', css_class='form-primary')
                    ),
                    Column(
                        FloatingField('hora_termino', css_class='form-primary')
                    ),
                ),
                Row(
                    Column(
                        FloatingField('tema', css_class='form-primary'),
                    ),
                    Column(
                        Div(
                            Switch('ministro_externo'),
                            FloatingField('ministro', css_class='form-primary'),
                            FloatingField('ministro_texto', css_class='form-primary'),
                        )
                    ),
                    css_class='align-items-end'
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
                        FloatingField('total_dizimos', css_class='form-primary money')
                    ),
                    Column(
                        FloatingField('total_ofertas', css_class='form-primary money')
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