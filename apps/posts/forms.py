from core.forms import FormBaseIxoye
from .models import Post, ArquivoPost
from django import forms
from crispy_bootstrap5.bootstrap5 import Switch
from crispy_forms.layout import Submit, Field

class ArquivoPostForm(FormBaseIxoye):
    class Meta:
        model = ArquivoPost
        fields = '__all__'
        widgets = {
            'post': forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

ArquivoPostFormSet = forms.modelformset_factory(ArquivoPost, fields=('arquivo',), extra=0)

class NewPostForm(FormBaseIxoye):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput(),
            'user': forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        categoria = kwargs.pop('categoria', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if instituicao:
            self.fields['instituicao'].initial = instituicao
        if categoria:
            self.helper['categoria'].wrap(Field, type="hidden", value=categoria)
        if user:
            self.fields['user'].initial = user

        self.fields['descricao'].label = ''
        self.fields['descricao'].widget.attrs['placeholder'] = "Descrição"

        self.helper['fixado'].wrap(Switch)
        self.helper['capa'].wrap(Field, template="core/includes/custom_capa_select.html")