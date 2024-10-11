from core.forms import FormBaseIxoye
from django import forms
from .models import Contribuicao, ContatosContribuicao
from django.forms import formset_factory

class ContribuicaoForm(FormBaseIxoye):
    class Meta:
        model = Contribuicao
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)

        if instituicao:
            self.fields['instituicao'].initial = instituicao