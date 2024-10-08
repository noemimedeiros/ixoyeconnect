from core.forms import FormBaseIxoye
from .models import CategoriaPost, Post
from django import forms
from crispy_bootstrap5.bootstrap5 import Switch
from crispy_forms.layout import Submit, Field

class NewPostForm(FormBaseIxoye):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput(),
            'categoria': forms.HiddenInput(),
            'user': forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        categoria = kwargs.pop('categoria', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper.form_tag = True
        self.helper.add_input(Submit('adicionar-post', 'Postar', css_class='button button-filled w-100'))

        if instituicao:
            self.fields['instituicao'].initial = instituicao
        if categoria:
            self.fields['categoria'].initial = categoria
        if user:
            self.fields['user'].initial = user

        self.fields['descricao'].label = ''
        self.fields['descricao'].widget.attrs['placeholder'] = "Descrição"

        self.helper['fixado'].wrap(Switch)
        self.helper['capa'].wrap(Field, template="posts/partials/custom_capa_select.html")