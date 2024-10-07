from core.forms import FormBaseIxoye
from .models import Post
from django import forms

class NewPostForm(FormBaseIxoye):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)

        if instituicao:
            self.fields['instituicao'].initial = instituicao
