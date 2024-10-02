from django import forms
from .models import Membro
from core.forms import FormBaseIxoye

class MembroForm(FormBaseIxoye):
    class Meta:
        model = Membro
        fields = ('ano_ingressao', )