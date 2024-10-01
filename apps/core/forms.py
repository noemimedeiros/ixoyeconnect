from allauth.account.forms import LoginForm, SignupForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div
from crispy_bootstrap5.bootstrap5 import FloatingField, Field

from core.models import Endereco

def floating_fields(self):
    self.helper = FormHelper(self)
    self.helper.form_show_labels = False
        
    field_layout = []
    for field_name, field in self.fields.items():
        if isinstance(field, forms.ModelChoiceField):
            field.empty_label = field.label

        field_classes = f'form-primary {field.widget.attrs.get('class')}'
        if isinstance(field, (forms.ModelChoiceField, forms.FileField, forms.ImageField)):
            field_layout.append(Field(field_name, css_class=field_classes))
        else:
            field_layout.append(FloatingField(field_name, css_class=field_classes))  

    self.helper.layout = Layout(*field_layout)

class FormBaseIxoye(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormBaseIxoye, self).__init__(*args, **kwargs)
        floating_fields(self)

class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self)

class SignUpForm(SignupForm):
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
            Row(
                Column(
                    FloatingField('bairro', css_class='form-primary'), css_class='col-lg-6 col-12'
                ),
                Column(
                    FloatingField('cidade', css_class='form-primary'), css_class='col-lg-6 col-12'
                ),
            ),
            Row(
                Column(
                    Field('uf', css_class='form-primary'), css_class='col-lg-6 col-12'
                ),
                Column(
                    FloatingField('numero', css_class='form-primary'), css_class='col-lg-6 col-12'
                )
            )
        )