from django import forms
from .models import AgendaSemanal, IconeAgendaSemanal
from core.forms import FormBaseIxoye
from crispy_forms.layout import Submit, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField

class AgendaSemanalForm(FormBaseIxoye):
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
        self.fields['dia_semana'].empty_label = None

        for id, field in enumerate(self.helper.layout.fields):
            if field.get_field_names()[0].name == 'icone':
                self.helper.layout.fields[id] = FloatingField('icone', template="partials/custom_icone_select.html")