from usuario.models import InstituicaoSede
from core.forms import FormBaseIxoye
from django import forms
from .models import Evento
from crispy_bootstrap5.bootstrap5 import Switch
from crispy_forms.layout import Submit, Field

class EventoForm(FormBaseIxoye):
    endereco_sede = forms.BooleanField(initial=False, label="Este evento ocorrerá na sede principal (endereço cadastrado)?")

    class Meta:
        model = Evento
        fields = '__all__'
        exclude = ('endereco',)
        widgets = {
            'instituicao': forms.HiddenInput(),
            'valor': forms.TextInput(attrs={"class": "money"}),
            'data': forms.DateInput(attrs={"class": "date"}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao')
        super().__init__(*args, **kwargs)

        if instituicao:
            self.fields['instituicao'].initial = instituicao

        self.helper['capa'].wrap(Field, template="core/includes/custom_capa_select.html")
        self.fields['valor'].localize = True

        self.helper['endereco_sede'].wrap(Switch)

        if self.instance.pk:
            if self.instance.endereco.pk == InstituicaoSede.objects.get(pk=instituicao).endereco.pk:
                self.fields['endereco_sede'].initial = True