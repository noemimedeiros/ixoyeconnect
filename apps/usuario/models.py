from datetime import date, datetime, timedelta
from itertools import chain
from operator import attrgetter
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db import connection, models
from django.db.models import Sum, Case, When, IntegerField, F
from PIL import Image
from core.models import Endereco
from django.contrib.auth.models import AbstractUser

data_atual = timezone.now()
mes_anterior_inicio = (data_atual - relativedelta(months=1)).replace(day=1)
mes_anterior_fim = data_atual.replace(day=1) - timezone.timedelta(days=1)

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
    logo = models.ImageField(max_length=100, null=False, blank=False, upload_to='instituicao/logo/', default="")

    def save(self, *args, **kwargs):
        super(InstituicaoSede, self).save(*args, **kwargs)
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

    def atividades(self):
        eventos = list(self.eventos.all()[:10])
        posts = list(self.posts.all()[:10])
        return sorted(chain(eventos, posts), key=attrgetter('data'), reverse=True)
    
    def proximo_evento(self):
        return self.eventos.filter(data__gte=data_atual).order_by('data', 'hora').first()

    def proxima_agenda(self):
        hoje_dia_semana = int((datetime.today().isoweekday() % 7) + 1)
        queryset = (
            self.agendas_semanais.annotate(
                proximidade=Case(
                    When(dia_semana__gte=hoje_dia_semana, then=F('dia_semana') - hoje_dia_semana),
                    default=7 - hoje_dia_semana + F('dia_semana'),
                    output_field=IntegerField(),
                )
            )
            .order_by('proximidade')
        )
        return queryset.first()
    
    def programacoes_hoje(self):
        dia_semana = str((datetime.today().isoweekday() % 7) + 1)
        programacoes = []
        if self.agendas_semanais.filter(dia_semana=dia_semana):
            programacoes += list(self.agendas_semanais.filter(dia_semana=dia_semana))
        if self.eventos.filter(data=datetime.today()):
            programacoes += list()
        return programacoes

    @property
    def quantidade_membros(self):
        with connection.cursor() as cursor:
            cursor.execute(f'''
            select count(*) from membro where sede_id = {self.pk}
            ''')
            row = cursor.fetchone()
            if row[0]:
                return row[0]
        return 0

    @property
    def ultimo_evento(self):
        return self.eventos.order_by('data', 'hora').last()
    
    @property
    def ultimo_post(self):
        return self.posts.order_by('data', 'hora').last()
    
    @property
    def relatorios_mes_atual(self):
        return self.relatorios.filter(data__month=timezone.now().month)
    
    @property
    def relatorios_mes_anterior(self):
        return self.relatorios.filter(data__range=(mes_anterior_inicio, mes_anterior_fim))
    
    @property
    def calcular_total(self):
        pessoas_mes_atual = (self.relatorios_mes_atual.aggregate(Sum('total_pessoas'))['total_pessoas__sum'] or 0)
        try:
            media_pessoas_mes_atual = int(pessoas_mes_atual/self.relatorios_mes_atual.count())
        except ZeroDivisionError:
            media_pessoas_mes_atual = 0

        pessoas_mes_anterior = (self.relatorios_mes_anterior.aggregate(Sum('total_pessoas'))['total_pessoas__sum'] or 0)
        try:
            media_pessoas_mes_anterior = int(pessoas_mes_anterior/self.relatorios_mes_anterior.count())
        except ZeroDivisionError:
            media_pessoas_mes_anterior = 0

        dizimos_mes_atual = (self.relatorios_mes_atual.aggregate(Sum('total_dizimos'))['total_dizimos__sum'] or 0)
        dizimos_mes_anterior = (self.relatorios_mes_anterior.aggregate(Sum('total_dizimos'))['total_dizimos__sum'] or 0)
        ofertas_mes_atual = (self.relatorios_mes_atual.aggregate(Sum('total_ofertas'))['total_ofertas__sum'] or 0)
        ofertas_mes_anterior = (self.relatorios_mes_anterior.aggregate(Sum('total_ofertas'))['total_ofertas__sum'] or 0)
        
        return {
            "media_pessoas_mes_atual": int(media_pessoas_mes_atual),
            "media_pessoas_mes_anterior": int(media_pessoas_mes_anterior),
            "dizimos_mes_atual": int(dizimos_mes_atual),
            "dizimos_mes_anterior": int(dizimos_mes_anterior),
            "ofertas_mes_atual": int(ofertas_mes_atual),
            "ofertas_mes_anterior": int(ofertas_mes_anterior),
        }
    
    @property
    def calcular_porcentagem(self):
        porcentagem_presenca_cultos = 0
        porcentagem_dizimo_cultos = 0
        porcentagem_oferta_cultos = 0

        try:
            porcentagem_presenca_cultos = ((self.calcular_total['media_pessoas_mes_atual'] - self.calcular_total['media_pessoas_mes_anterior']) / self.calcular_total['media_pessoas_mes_anterior']) * 100
        except ZeroDivisionError:
            porcentagem_presenca_cultos = 0
        try:
            porcentagem_dizimo_cultos = ((self.calcular_total['dizimos_mes_atual'] - self.calcular_total['dizimos_mes_anterior']) / self.calcular_total['dizimos_mes_anterior']) * 100
        except ZeroDivisionError:
            porcentagem_dizimo_cultos = 0
        try:
            porcentagem_oferta_cultos = ((self.calcular_total['ofertas_mes_atual'] - self.calcular_total['ofertas_mes_anterior']) / self.calcular_total['ofertas_mes_anterior']) * 100
        except ZeroDivisionError:
            porcentagem_oferta_cultos = 0 
        
        return {
            "presenca_cultos": int(porcentagem_presenca_cultos),
            "dizimo_cultos": int(porcentagem_dizimo_cultos),
            "oferta_cultos": int(porcentagem_oferta_cultos),
        }

    @property
    def porcentagem_distribuicao_participantes(self):
        total_pessoas = (self.relatorios.aggregate(Sum('total_pessoas'))['total_pessoas__sum'] or 0)
        total_mulheres = (self.relatorios.aggregate(Sum('total_mulheres'))['total_mulheres__sum'] or 0)
        total_homens = (self.relatorios.aggregate(Sum('total_homens'))['total_homens__sum'] or 0)
        total_jovens = (self.relatorios.aggregate(Sum('total_jovens'))['total_jovens__sum'] or 0)
        total_juniores = (self.relatorios.aggregate(Sum('total_juniores'))['total_juniores__sum'] or 0)
        total_visitantes = (self.relatorios.aggregate(Sum('total_visitantes'))['total_visitantes__sum'] or 0)

        try:
            porcentagem_mulheres = (total_mulheres / total_pessoas) * 100
        except ZeroDivisionError:
            porcentagem_mulheres = 0
        try:
            porcentagem_homens = (total_homens / total_pessoas) * 100
        except ZeroDivisionError:
            porcentagem_homens = 0
        try:
            porcentagem_jovens = (total_jovens / total_pessoas) * 100
        except ZeroDivisionError:
            porcentagem_jovens = 0
        try:
            porcentagem_juniores = (total_juniores / total_pessoas) * 100
        except ZeroDivisionError:
            porcentagem_juniores = 0
        try:
            porcentagem_visitantes = (total_visitantes / total_pessoas) * 100
        except ZeroDivisionError:
            porcentagem_visitantes = 0
        
        return {
            "homens": int(porcentagem_homens),
            "mulheres": int(porcentagem_mulheres),
            "jovens": int(porcentagem_jovens),
            "juniores": int(porcentagem_juniores),
            "visitantes": int(porcentagem_visitantes),
        }
    
    @property
    def grafico_entradas(self):
        relatorios = self.relatorios.all().order_by('data')
        grafico = {
            'data': [],
            'valor': []
        }
        for i in range(0, len(relatorios[:7]), 1):
            try:
                data = datetime.strftime(relatorios[i].data, '%d %b')
                soma = (relatorios[i].total_dizimos or 0) + (relatorios[i].total_ofertas or 0)
                grafico['data'].append(data)
                grafico['valor'].append(soma)
            except Exception as e:
                print(e)
        return grafico

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
        if membro_ha == 1:
            return f'{membro_ha} ano'
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
            return self.escalas.filter(data__gte=data_atual).order_by('-data').last()
        return None

    def ultimas_notificacoes(self):
        return self.user.notificacoes.all()[:3]

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
    instituicao = models.ForeignKey(InstituicaoSede, on_delete=models.CASCADE, null=True, blank=True)
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