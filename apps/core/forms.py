from allauth.account.forms import LoginForm, SignupForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div
from crispy_bootstrap5.bootstrap5 import FloatingField, Field, Switch

from core.models import Endereco

def floating_fields(self):
    self.helper = FormHelper(self)
    self.helper.form_tag = False
        
    layout_fields = []
    
    for field_name, field in self.fields.items():
        field_widget = field.widget.__class__.__name__
        field_classes = f'form-primary {field.widget.attrs.get('class')}'
        if field_widget in ['TextInput', 'NumberInput', 'EmailInput', 'URLInput', 'DateInput', 'Select', 'PasswordInput']:
            layout_fields.append(FloatingField(field_name, css_class=field_classes))
        elif field_widget in ['ClearableFileInput', 'FileInput', 'Textarea']:
            layout_fields.append(Field(field_name, css_class=field_classes))
        else:
            layout_fields.append(Field(field_name))
        
        if field_widget == 'Select':
            field.empty_label = field.label
            field.label = ''

    # Aplica o layout
    self.helper.layout = Layout(*layout_fields)

class FormBaseIxoye(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormBaseIxoye, self).__init__(*args, **kwargs)
        floating_fields(self)

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self)

class MySignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self)

class EnderecoForm(FormBaseIxoye):
    class Meta:
        model = Endereco
        fields = '__all__'
        widgets = {
            'cep': forms.TextInput(attrs={'class': 'cep'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField('cep', css_class='form-primary cep'), css_class='col-lg-4 col-12'
                ),
                Column(
                    FloatingField('rua', css_class='form-primary'), css_class='col-lg-8 col-12'
                )
            ),
            FloatingField('complemento', css_class='form-primary'),
            FloatingField('bairro', css_class='form-primary'),
            FloatingField('cidade', css_class='form-primary'),
            Row(
                Column(
                    Field('uf', css_class='form-primary'), css_class='col-lg-6 col-12'
                ),
                Column(
                    FloatingField('numero', css_class='form-primary'), css_class='col-lg-6 col-12'
                )
            )
        )