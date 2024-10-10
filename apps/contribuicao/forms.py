from core.forms import FormBaseIxoye
from django import forms
from .models import Contribuicao, ContatosContribuicao
from django.forms import formset_factory

class ContribuicaoForm(FormBaseIxoye):
    class Meta:
        model = Contribuicao
        fields = '__all__'
        widgets = {
            'instituicao'
        }