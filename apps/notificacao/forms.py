from django import forms
from core.forms import FormBaseIxoye
from .models import ConfiguracoesNotificacao
from crispy_forms.layout import Layout, Div, HTML, Column, Row
from crispy_bootstrap5.bootstrap5 import Switch, FloatingField

class ConfiguracoesNotificacaoForm(FormBaseIxoye):
    class Meta:
        model = ConfiguracoesNotificacao
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'silenciar_inicio': forms.TextInput(attrs={'class': 'datepicker date'}),
            'silenciar_fim': forms.TextInput(attrs={'class': 'datepicker date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['user'].initial = user

        self.helper['habilitado'].wrap(Switch)
        self.helper.layout = Layout(
            Div(
                HTML('<h6 class="profile-infos-title">Ativar ou desativar todas as notificações.</h6>'),
                Switch('habilitado', css_class=""), css_class="profile-infos-div"),
            Div(
                HTML('<h6 class="profile-infos-title">Configure o período em que prefere receber as notificações.</h6>'),
                FloatingField('horario', css_class="form-primary"), css_class="profile-infos-div"),
            Div(
                HTML('<h6 class="profile-infos-title"><b>Opção para silenciar notificações temporariamente por um período definido.</b></h6>'),
                Row(
                    Column(FloatingField('silenciar_inicio', css_class="form-primary datepicker date")),
                    Column(FloatingField('silenciar_fim', css_class="form-primary datepicker date"))
                ),css_class="profile-infos-div")
        )

    def clean(self):
        cleaned_data = super().clean()
        silenciar_inicio = cleaned_data.get('silenciar_inicio', None)
        silenciar_fim = cleaned_data.get('silenciar_fim', None)

        if (silenciar_inicio and not silenciar_fim) or (silenciar_fim and not silenciar_inicio):
            self.add_error('silenciar_fim', 'Ao selecionar uma data de período para silenciar as notificações, os dois campos devem ser preenchidos.')
        
        if silenciar_fim and silenciar_inicio:
            if silenciar_inicio > silenciar_fim:
                self.add_error('silenciar_fim', 'A data de início deve ser anterior a data final do período.')

        return cleaned_data