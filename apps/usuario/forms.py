from typing import Any
from django import forms
from core.forms import FormBaseIxoye
from .models import Instituicao, InstituicaoSede, Membro
from crispy_forms.layout import Submit, Layout, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField, Field

class InstituicaoForm(FormBaseIxoye):
    class Meta:
        model = Instituicao
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.form_action = '/usuario/cadastrar_instituicao/'
        self.helper.add_input(Submit('submit', 'Cadastrar Instituicao', css_class="button button-filled w-100"))

class InstituicaoSedeForm(FormBaseIxoye):
    class Meta:
        model = InstituicaoSede
        fields = "__all__"
        exclude = ('user', 'instituicao', 'endereco', 'capa', 'codigo', )
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'phone'}),
            'cnpj': forms.TextInput(attrs={'class': 'cnpj'})
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
            'data_nascimento': forms.TextInput(attrs={'class': 'date'}),
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