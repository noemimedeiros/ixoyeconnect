from .models import AgendaSemanal
from core.forms import FormBaseIxoye
from crispy_forms.layout import Submit

class AgendaSemanalForm(FormBaseIxoye):
    class Meta: 
        model = AgendaSemanal
        fields = '__all__'
        exclude = ('instituicao', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Adicionar agenda', css_class='button button-filled'))
        self.fields['dia_semana'].empty_label = None