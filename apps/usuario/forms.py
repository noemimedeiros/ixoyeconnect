from core.forms import FormBaseIxoye
from .models import Usuario

class UsuarioForm(FormBaseIxoye):
    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ('endereco',)