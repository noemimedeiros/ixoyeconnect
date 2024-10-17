from django import forms
from django.forms import modelformset_factory
from core.forms import FormBaseIxoye
from django.db.models import Q
from .models import (Denominacao, Departamento, Funcao, FuncaoDepartamento, FuncaoMembro, Instituicao,
                     InstituicaoSede, Membro, RedeSocialInstituicaoSede, User)
from crispy_forms.layout import Submit
from crispy_bootstrap5.bootstrap5 import FloatingField, Switch

class UserForm(FormBaseIxoye):
    class Meta:
        model = User
        fields = ('email', 'username',)

class DenominacaoForm(FormBaseIxoye):
    class Meta:
        model = Denominacao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.form_action = '/usuario/cadastrar_denominacao/'
        self.helper.add_input(Submit('adicionar-denominacao', 'Adicionar Denominação', css_class='button button-filled w-100'))

class InstituicaoForm(FormBaseIxoye):
    class Meta:
        model = Instituicao
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.form_action = '/usuario/cadastrar_instituicao/'
        self.helper.add_input(Submit('adicionar-instituicao', 'Cadastrar Instituicao', css_class="btn button-filled w-100"))

        for id, field in enumerate(self.helper.layout.fields):
            if field.get_field_names()[0].name == 'denominacao':
                self.helper.layout.fields[id] = FloatingField('denominacao', template="usuario/partials/custom_denominacao_select.html")

class InstituicaoSedeForm(FormBaseIxoye):
    class Meta:
        model = InstituicaoSede
        fields = "__all__"
        exclude = ('user', 'endereco', 'codigo', )
        widgets = {
            'celular': forms.TextInput(attrs={'class': 'phone'}),
            'cnpj': forms.TextInput(attrs={'class': 'cnpj'}),
            'instituicao': forms.HiddenInput()
        }
        error_messages = {
            'cnpj': {
                'unique': "Já existe um cadastro com esse cnpj. Por favor, verifique se você inseriu corretamente.",
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MembroForm(FormBaseIxoye):
    codigo_sede = forms.CharField(required=True, max_length=8, label="Código da sua Igreja")

    class Meta:
        model = Membro
        fields = '__all__'
        exclude = ('user', 'endereco', 'foto', 'sede', 'desvinculado', 'admin', )
        widgets = {
            'data_nascimento': forms.TextInput(attrs={'class': 'datepicker date'}),
            'celular': forms.TextInput(attrs={'class': 'phone'})
        }

    def clean(self):
        cleaned_data = super().clean()
        
        ano_ingressao = cleaned_data.get('ano_ingressao')
        if ano_ingressao < 1900 or ano_ingressao > 2100:
            self.add_error('ano', 'Por favor, verifique se o ano que você inseriu é válido.')

        try:
            InstituicaoSede.objects.get(codigo=self.cleaned_data['codigo_sede'])
        except InstituicaoSede.DoesNotExist:
            self.add_error('codigo_sede', "Código incorreto ou inexistente. Por favor, verifique se seu código está correto e tente novamente.")

        return cleaned_data
    
class NewMembroForm(FormBaseIxoye):
    class Meta:
        model = Membro
        fields = '__all__'
        exclude = ('user', 'endereco', 'desvinculado', )
        widgets = {
            'user': forms.HiddenInput(),
            'data_nascimento': forms.TextInput(attrs={'class': 'datepicker date'}),
            'celular': forms.TextInput(attrs={'class': 'phone'}),
            'sede': forms.HiddenInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        
        ano_ingressao = cleaned_data.get('ano_ingressao')
        if ano_ingressao < 1900 or ano_ingressao > 2100:
            self.add_error('ano', 'Por favor, verifique se o ano que você inseriu é válido.')

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        sede = kwargs.pop('sede', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if sede:
            self.fields['sede'].initial = sede
            self.fields['sede'].queryset = InstituicaoSede.objects.filter(pk=sede)

        self.fields['data_nascimento'].localize = True
        self.helper['admin'].wrap(Switch)

        if user and not user.is_admin:
            self.fields.pop('admin')
    
class DepartamentoForm(FormBaseIxoye):
    class Meta:
        model = Departamento
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.form_action = '/usuario/cadastrar_departamento/'
        self.helper.add_input(Submit('adicionar-departamento', 'Criar Departamento', css_class='btn button-filled w-100'))

        if instituicao:
            self.fields['instituicao'].queryset = InstituicaoSede.objects.filter(pk=instituicao.pk)
            self.fields['instituicao'].initial = instituicao

class FuncaoForm(FormBaseIxoye):
    class Meta:
        model = Funcao
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.form_action = '/usuario/cadastrar_funcao/'
        self.helper.add_input(Submit('adicionar-funcao', 'Criar Cargo/Função', css_class='btn button-filled w-100'))

        if instituicao:
            self.fields['instituicao'].queryset = InstituicaoSede.objects.filter(pk=instituicao.pk)
            self.fields['instituicao'].initial = instituicao

class FuncaoMembroForm(FormBaseIxoye):
    class Meta:
        model = FuncaoMembro
        fields = '__all__'
        widgets = {
            'membro': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        membro = kwargs.pop('membro', None)
        super().__init__(*args, **kwargs)

        if membro:
            self.fields['membro'].initial = membro
            self.fields['membro'].queryset = Membro.objects.filter(pk=membro.pk)

        self.fields['departamento'].queryset = Departamento.objects.filter(Q(instituicao__isnull=True) | Q(instituicao=membro.sede.pk))
        funcoes = FuncaoDepartamento.objects.filter(departamento_id=1)
        self.fields['funcao'].queryset = Funcao.objects.filter(pk__in=funcoes.values_list('pk', flat=True))

        if self.instance.pk:
            funcoes = FuncaoDepartamento.objects.filter(departamento_id=self.instance.departamento.id)
            self.fields['funcao'].queryset = Funcao.objects.filter(pk__in=funcoes.values_list('funcao_id', flat=True))

        if self.is_bound:
            self.fields['funcao'].queryset = Funcao.objects.all()

        # self.helper['departamento'].wrap(Field, template="usuario/partials/custom_departamento_field.html")
        # self.helper['funcao'].wrap(Field, template="usuario/partials/custom_funcao_field.html")

FuncaoMembroFormset = modelformset_factory(FuncaoMembro, FuncaoMembroForm, can_delete=True, extra=1)
    
class RedeSocialInstituicaoSedeForm(FormBaseIxoye):
    class Meta:
        model = RedeSocialInstituicaoSede
        fields = '__all__'
        widgets = {
            'instituicao': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)

        if instituicao:
            self.fields['instituicao'].queryset = InstituicaoSede.objects.filter(pk=instituicao.pk)
            self.fields['instituicao'].initial = instituicao

RedeSocialInstituicaoSedeFormset = modelformset_factory(RedeSocialInstituicaoSede, RedeSocialInstituicaoSedeForm, can_delete=True, extra=1)