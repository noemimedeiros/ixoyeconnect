from usuario.models import InstituicaoSede
from core.forms import FormBaseIxoye
from django import forms
from .models import METODO_CONTRIBUICAO, TIPO_CONTRIBUICAO, Contribuicao, ContatosContribuicao
from crispy_forms.layout import Field
from crispy_bootstrap5.bootstrap5 import Switch
from django.forms import modelformset_factory

class ContribuicaoForm(FormBaseIxoye):
    tipo = forms.ChoiceField(choices=TIPO_CONTRIBUICAO)
    metodo = forms.ChoiceField(choices=METODO_CONTRIBUICAO)

    relacionar_departamento = forms.BooleanField(initial=False, label="Relacionar esta contribuição à um departamento.", required=False)

    class Meta:
        model = Contribuicao
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False

        if instituicao:
            self.fields['instituicao'].queryset = InstituicaoSede.objects.filter(pk=instituicao.pk)
            self.fields['instituicao'].initial = instituicao

        self.helper['departamento'].wrap(Field, template="contribuicao/partials/custom_departamento_field.html")
        self.helper['relacionar_departamento'].wrap(Switch)

        if self.instance.pk:
            if self.instance.departamento:
                self.fields['relacionar_departamento'].initial = True

    def clean(self):
        cleaned_data = super().clean()
        metodo = cleaned_data.get('metodo')
        chave_pix = cleaned_data.get('chave_pix')
        banco = cleaned_data.get('banco')
        conta = cleaned_data.get('conta')
        agencia = cleaned_data.get('agencia')


        if metodo == "pix" and not chave_pix:
            self.add_error('chave_pix', 'Este campo é obrigatório.')
        elif metodo == "deposito":
            if not banco:
                self.add_error('banco', 'Este campo é obrigatório.')
            if not agencia:
                self.add_error('agencia', 'Este campo é obrigatório.')
            if not conta:
                self.add_error('conta', 'Este campo é obrigatório.')

        return cleaned_data