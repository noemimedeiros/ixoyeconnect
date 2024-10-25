from datetime import date
from django.utils import timezone
from django.db import connection, models
from PIL import Image
from core.models import Endereco
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        return self.conta.nome
    
    @property
    def is_instituicao(self):
        if hasattr(self, 'instituicaosede'):
            return True
        else:
            return False
    
    @property
    def is_admin(self):
        if hasattr(self, 'instituicaosede') or self.membro.admin:
            return True
        else:
            return False
    
    @property
    def profile_picture(self):
        if self.is_instituicao:
            return self.conta.logo
        else:
            return self.conta.foto

    @property
    def conta(self):
        if self.is_instituicao:
            return self.instituicaosede
        else:
            return self.membro

    @property
    def instituicao(self):
        if self.is_instituicao:
            return self.conta
        else:
            return self.conta.sede
        
    @property
    def get_quant_notificacoes(self):
        with connection.cursor() as cursor:
            cursor.execute(f'select count(*) from notificacao where user_id = {self.pk} and lida = 0')
            row = cursor.fetchone()
            if row[0]:
                return int(row[0])
        return 0

class Denominacao(models.Model):
    nome = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'denominacao'

class Instituicao(models.Model):
    nome = models.CharField(max_length=120, null=False, blank=False)
    denominacao = models.ForeignKey(Denominacao, on_delete=models.CASCADE, null=False, blank=False)
    sigla = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "instituicao"

class UsuarioAbstract(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    nome = models.CharField(max_length=60, null=False, blank=False, verbose_name="Nome Completo")
    celular = models.CharField(max_length=16, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Endereço")

    class Meta:
        abstract = True

class InstituicaoSede(UsuarioAbstract):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=False, blank=False)
    cnpj = models.CharField(max_length=20, null=False, blank=False, unique=True)
    sigla = models.CharField(max_length=10, null=False, blank=False)
    codigo = models.CharField(max_length=8, null=False, blank=False, unique=True)
    logo = models.ImageField(max_length=100, null=False, blank=False, upload_to='instituicao/logo/')

    def save(self, *args, **kwargs):
        super(Membro, self).save(*args, **kwargs)
        if self.logo:
            img = Image.open(self.logo.path)
            width, height = img.size
            TARGET_WIDTH = 300
            coefficient = width / 300
            new_height = height / coefficient
            img = img.resize((int(TARGET_WIDTH),int(new_height)), Image.Resampling.LANCZOS)
            img.save(self.logo.path,quality=80,optimize=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "instituicaosede"

    @property
    def quantidade_membros(self):
        with connection.cursor() as cursor:
            cursor.execute(f'''
            select count(*) from membro where sede = {self.pk}
            ''')
            row = cursor.fetchall()
            if row[0]:
                return row[0]
        return 0

class RedeSocial(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'redesocial'

class RedeSocialInstituicaoSede(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False, related_name='redes_sociais')
    redesocial = models.ForeignKey(RedeSocial, on_delete=models.CASCADE, null=False, blank=False)
    descricao = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'redesocialinstituicaosede'

class Membro(UsuarioAbstract):
    sede = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=False, blank=False)
    ano_ingressao = models.IntegerField(null=True, blank=True)
    data_nascimento = models.DateField(null=False, blank=False)
    foto = models.ImageField(upload_to='usuario/perfil', max_length=255, null=True, blank=True)
    desvinculado = models.BooleanField(default=0)
    admin = models.BooleanField(default=False, verbose_name="Definir como Admin", help_text="Ao definir um usuário como admin, ele poderá ter acesso a publicar, editar ou excluir informações da Igreja.")

    class Meta:
        db_table = 'membro'

    def __str__(self):
        return self.nome
    
    @property
    def primeiro_nome(self):
        return self.nome.split(" ")[0]
    
    def save(self, *args, **kwargs):
        super(Membro, self).save(*args, **kwargs)
        if self.foto:
            img = Image.open(self.foto.path)
            width, height = img.size
            TARGET_WIDTH = 300
            coefficient = width / 300
            new_height = height / coefficient
            img = img.resize((int(TARGET_WIDTH),int(new_height)), Image.Resampling.LANCZOS)
            img.save(self.foto.path,quality=80,optimize=True)

    @property
    def idade(self):
        today = timezone.now().date()
        idade = int(
            today.year
            - (self.data_nascimento.year)
            - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        )
        return idade
    
    @property
    def membro_ha(self):
        today = timezone.now().date()
        membro_ha = int(
            today.year
            - (self.ano_ingressao)
        )
        if membro_ha <= 0:
            return f'{membro_ha} meses'
        return f'{membro_ha} anos'
    
    def get_funcoes(self):
        funcoes = [str(funcao) for funcao in self.funcoes.all()]
        if funcoes:
            funcoes = " - ".join(funcoes)
            return funcoes
        return "Membro"
    
    def eventos_confirmados_pks(self):
        return self.eventos_confirmados.values_list("evento", flat=True)
    
    def proxima_escala(self):
        if self.escalas.all():
            return self.escalas.filter(data__gte=date.today()).order_by('-data').last()
        return None

class Funcao(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=True, blank=True)
    funcao = models.CharField(max_length=50, null=False, blank=False, verbose_name="Nome da Função")
    descricao = models.TextField(null=True, blank=True, help_text="Este campo é opcional")

    def __str__(self):
        return self.funcao
     
    class Meta:
        db_table = 'funcao'

class Departamento(models.Model):
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=True, blank=True)
    departamento = models.CharField(max_length=50, null=False, blank=False, verbose_name="Nome do Departamento")
    descricao = models.TextField(null=True, blank=True, help_text="Este campo é opcional")

    def __str__(self):
        return self.departamento

    class Meta:
        db_table = 'departamento'

class FuncaoDepartamento(models.Model):
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, null=False, blank=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'funcaodepartamento'

    def __str__(self):
        return f'{self.funcao} - {self.departamento}'

class FuncaoMembro(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, null=False, blank=False, related_name="funcoes")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, blank=False)
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'funcaomembro'

    def __str__(self):
        return f'{self.funcao} - {self.departamento}'