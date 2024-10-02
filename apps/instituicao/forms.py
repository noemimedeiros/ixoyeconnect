from django import forms
from core.forms import FormBaseIxoye
from .models import Instituicao, InstituicaoSede
from crispy_forms.layout import Layout, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField, Field

class InstituicaoForm(FormBaseIxoye):
    class Meta:
        model = Instituicao
        fields = "__all__"

class InstituicaoSedeForm(FormBaseIxoye):
    class Meta:
        model = InstituicaoSede
        fields = "__all__"
        exclude = ('user', 'instituicao', 'endereco', 'capa', )
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'phone'}),
            'cnpj': forms.TextInput(attrs={'class': 'cnpj'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)