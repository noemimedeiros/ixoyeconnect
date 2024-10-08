from django import forms
from .models import DIAS_SEMANA, AgendaSemanal, IconeAgendaSemanal
from core.forms import FormBaseIxoye
from crispy_forms.layout import Submit, Layout, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField

class AgendaSemanalForm(FormBaseIxoye):
    dia_semana = forms.ChoiceField(choices=DIAS_SEMANA, required=True)
    class Meta: 
        model = AgendaSemanal
        fields = '__all__'
        widgets = {
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'instituicao': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        instituicao = kwargs.pop('instituicao', None)
        super().__init__(*args, **kwargs)

        if instituicao:
            self.fields['instituicao'].initial = instituicao

        self.helper.form_tag = True
        self.helper.add_input(Submit('adicionar-agenda', 'Adicionar agenda', css_class='button button-filled w-100'))
        
        self.helper['icone'].wrap(FloatingField, template="agenda/partials/custom_icone_select.html")

        # self.helper.layout = Layout(
        #     Row(
        #         Column(FloatingField('titulo', css_class='form-primary form-control'), css_class='col-lg-4 col-12'),
        #         Column(FloatingField('dia_semana', css_class='form-primary'), css_class='col-lg-4 col-12'),
        #         Column(FloatingField('hora', css_class='form-primary form-control'), css_class='col-lg-4 col-12'),
        #         Column(FloatingField('icone', template="partials/custom_icone_select.html"), css_class='col-lg-3 col-md-4 col-12'),
        #         Column(FloatingField('descricao', css_class='form-primary form-control'), css_class='col-lg-9 col-12')
        #     )
        # )