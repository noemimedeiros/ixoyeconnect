from core.forms import FormBaseIxoye
from django import forms
from .models import Evento
from crispy_forms.layout import Submit, Field

class EventoForm(FormBaseIxoye):
    class Meta:
        model = Evento
        fields = '__all__'
        exclude = ('endereco',)
        widgets = {
            'instituicao': forms.HiddenInput(),
            'valor': forms.TextInput(attrs={"class": "money"})
        }
    
    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao')
        super().__init__(*args, **kwargs)

        if instituicao:
            self.fields['instituicao'].initial = instituicao

        self.helper['capa'].wrap(Field, template="core/includes/custom_capa_select.html")
        self.fields['valor'].localize = True