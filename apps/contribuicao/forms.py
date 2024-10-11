from usuario.models import Instituicao
from core.forms import FormBaseIxoye
from django import forms
from .models import METODO_CONTRIBUICAO, TIPO_CONTRIBUICAO, Contribuicao, ContatosContribuicao
from crispy_forms.layout import Field

class ContribuicaoForm(FormBaseIxoye):
    metodo = forms.ChoiceField(choices=METODO_CONTRIBUICAO)
    tipo = forms.ChoiceField(choices=TIPO_CONTRIBUICAO)

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
            self.fields['instituicao'].queryset = Instituicao.objects.filter(pk=instituicao.pk)
            self.fields['instituicao'].initial = instituicao

        self.helper['departamento'].wrap(Field, template="contribuicao/partials/custom_departamento_field.html")

class ContatosContribuicaoForm(FormBaseIxoye):
    class Meta:
        model = ContatosContribuicao
        fields = '__all__'
        widgets = {
            'contribuicao': forms.HiddenInput(),
            'telefone': forms.TextInput(attrs={'class': 'phone'})
        }
    def __init__(self, *args, **kwargs):
        contribuicao = kwargs.pop('contribuicao', None)
        super().__init__(*args, **kwargs)

        if contribuicao:
            self.fields['contribuicao'].initial = contribuicao