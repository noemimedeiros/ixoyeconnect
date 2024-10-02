from core.forms import FormBaseIxoye
from .models import Usuario
from django import forms

class UsuarioForm(FormBaseIxoye):
    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ('user', 'endereco',)
        widgets = {
            'celular': forms.TextInput(attrs={'class': 'phone'}),
            'data_nascimento': forms.TextInput(attrs={'class': 'date'})
        }