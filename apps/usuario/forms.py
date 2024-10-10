from typing import Any
from django import forms
from core.forms import FormBaseIxoye
from .models import Denominacao, Instituicao, InstituicaoSede, Membro
from crispy_forms.layout import Submit, Layout, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField, Field

class DenominacaoForm(FormBaseIxoye):
    class Meta:
        model = Denominacao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.form_action = '/usuario/cadastrar_denominacao/'
        self.helper.add_input(Submit('adicionar-denominacao', 'Adicionar Denominação', css_class='button button-filled w-100'))

class InstituicaoForm(FormBaseIxoye):
    class Meta:
        model = Instituicao
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.form_action = '/usuario/cadastrar_instituicao/'
        self.helper.add_input(Submit('adicionar-instituicao', 'Cadastrar Instituicao', css_class="btn button-filled w-100"))

        for id, field in enumerate(self.helper.layout.fields):
            if field.get_field_names()[0].name == 'denominacao':
                self.helper.layout.fields[id] = FloatingField('denominacao', template="usuario/custom_denominacao_select.html")

class InstituicaoSedeForm(FormBaseIxoye):
    class Meta:
        model = InstituicaoSede
        fields = "__all__"
        exclude = ('user', 'endereco', 'capa', 'codigo', )
        widgets = {
            'celular': forms.TextInput(attrs={'class': 'phone'}),
            'cnpj': forms.TextInput(attrs={'class': 'cnpj'}),
            'instituicao': forms.HiddenInput()
        }
        error_messages = {
            'cnpj': {
                'unique': "Já existe um cadastro com esse cnpj. Por favor, verifique se você inseriu corretamente.",
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MembroForm(FormBaseIxoye):
    codigo_sede = forms.CharField(required=True, max_length=8, label="Código da sua Igreja")

    class Meta:
        model = Membro
        fields = '__all__'
        exclude = ('user', 'endereco', 'foto', 'sede', )
        widgets = {
            'data_nascimento': forms.TextInput(attrs={'class': 'datepicker date'}),
            'celular': forms.TextInput(attrs={'class': 'phone'})
        }

    def clean(self):
        cleaned_data = super().clean()
        
        ano_ingressao = cleaned_data.get('ano_ingressao')
        if ano_ingressao < 1900 or ano_ingressao > 2100:
            self.add_error('ano', 'Por favor, verifique se o ano que você inseriu é válido.')

        try:
            InstituicaoSede.objects.get(codigo=self.cleaned_data['codigo_sede'])
        except InstituicaoSede.DoesNotExist:
            self.add_error('codigo_sede', "Código incorreto ou inexistente. Por favor, verifique se seu código está correto e tente novamente.")

        return cleaned_data