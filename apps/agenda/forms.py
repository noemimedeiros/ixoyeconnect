from django import forms
from .models import AgendaSemanal, IconeAgendaSemanal
from core.forms import FormBaseIxoye
from crispy_forms.layout import Submit, Layout, Row, Column
from crispy_bootstrap5.bootstrap5 import FloatingField

class AgendaSemanalForm(FormBaseIxoye):
    DIAS_SEMANA = (
        ('domingo', 'Domingo'),
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
    )
    dia_semana = forms.ChoiceField(choices=DIAS_SEMANA, required=True)
    class Meta: 
        model = AgendaSemanal
        fields = '__all__'
        exclude = ('instituicao', )
        widgets = {
            'hora': forms.TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Adicionar agenda', css_class='button button-filled'))
        
        for id, field in enumerate(self.helper.layout.fields):
            if field.get_field_names()[0].name == 'icone':
                self.helper.layout.fields[id] = FloatingField('icone', template="partials/custom_icone_select.html")

        # self.helper.layout = Layout(
        #     Row(
        #         Column(FloatingField('titulo', css_class='form-primary form-control'), css_class='col-lg-4 col-12'),
        #         Column(FloatingField('dia_semana', css_class='form-primary'), css_class='col-lg-4 col-12'),
        #         Column(FloatingField('hora', css_class='form-primary form-control'), css_class='col-lg-4 col-12'),
        #         Column(FloatingField('icone', template="partials/custom_icone_select.html"), css_class='col-lg-3 col-md-4 col-12'),
        #         Column(FloatingField('descricao', css_class='form-primary form-control'), css_class='col-lg-9 col-12')
        #     )
        # )