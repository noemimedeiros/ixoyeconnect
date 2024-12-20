from django.urls import reverse_lazy
from usuario.models import FuncaoMembro, InstituicaoSede, Membro
from core.forms import FormBaseIxoye
from django import forms
from .models import Escala
from crispy_forms.layout import Submit

class EscalaForm(FormBaseIxoye):
    class Meta:
        model = Escala
        fields = '__all__'
        exclude = ('confirmado', )
        widgets = {
            'instituicao': forms.HiddenInput(),
            'data': forms.DateInput(attrs={'class': 'date datepicker'}),
            'hora': forms.TimeInput(attrs={'type': 'time'})
        }
    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)

        self.helper.form_action = reverse_lazy('escala:escala_create_view', kwargs={'instituicao_pk': instituicao.pk})
        self.helper.form_tag = True
        self.helper.add_input(Submit('adicionar-escala', 'Criar Escala', css_class="btn button-filled w-100"))

        if instituicao:
            self.fields['instituicao'].initial = instituicao.pk
            self.fields['instituicao'].queryset = InstituicaoSede.objects.filter(pk=instituicao.pk)

        funcoes_membros = FuncaoMembro.objects.filter(membro__sede_id=instituicao.pk).values_list('membro_id', flat=True)
        self.fields['membro'].queryset = Membro.objects.filter(pk__in=funcoes_membros)
        if not self.is_bound:
            self.fields['funcao_membro'].queryset = FuncaoMembro.objects.none()