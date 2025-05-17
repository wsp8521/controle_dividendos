from decimal import Decimal
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

####################################### SETOR #############################################
class SetorAtivo(models.Model):
    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setor"
        ordering = ['-id']
        
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_setor", null=True)
    setor = models.CharField(max_length=20, verbose_name='setor')
    setor_classe = models.CharField(max_length=20, verbose_name='classe', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    def __str__(self):
        return self.setor

####################################### ATIVO #############################################
class Ativos(models.Model):
    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"
        ordering = ['ativo']

    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ativo", null=True)
    ativo = models.CharField(max_length=250, verbose_name='nome do ativo')
    ticket = models.CharField(max_length=10)
    classe = models.CharField(max_length=10)
    cnpj = models.CharField(max_length=20, verbose_name='CNPJ')
    setor = models.ForeignKey(SetorAtivo, on_delete=models.CASCADE, related_name="setor_ativo", verbose_name='Setor', null=True, blank=True, default=None)
    corretora = models.ForeignKey('Corretora', on_delete=models.CASCADE, related_name='ativos_corretora', null=True, blank=True, verbose_name='Corretora')
    qtdAtivo = models.IntegerField(verbose_name='Qtd', blank=True, null=True)
    investimento = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    dividendos = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    def __str__(self):
        return self.ticket

####################################### PROVENTOS #############################################
class Proventos(models.Model):
    class Meta:
        verbose_name = "Proventos"
        verbose_name_plural = "Proventos"
        ordering = ['-data_pgto']

    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_provento", null=True)
    id_ativo = models.ForeignKey(Ativos, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ativos")
    classe = models.CharField(max_length=10)
    status = models.CharField(max_length=10, default="A PAGAR")
    tipo_provento = models.CharField(max_length=20, verbose_name='tipo de provento')
    valor_recebido = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='valor recebido')
    data_pgto = models.DateField(verbose_name='data do pagamento')
    ano = models.IntegerField(verbose_name='ano', null=True, blank=True)
    mes = models.CharField(max_length=15, verbose_name='mês', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    def save(self, *args, **kwargs):
        if self.data_pgto:
            self.ano = self.data_pgto.year
            self.mes = self.data_pgto.month
            self.status = "PAGO" if self.data_pgto <= now().date() else "A PAGAR"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id_ativo.ticket if self.id_ativo else "Ativo excluído"} - {self.classe}'

####################################### OPERACAO #############################################
class Operacao(models.Model):
    class Meta:
        verbose_name = "Operação"
        verbose_name_plural = "Operação"
        ordering = ['-data_operacao']

    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_operacao", null=True)
    id_ativo = models.ForeignKey(Ativos, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ativo')
    classe = models.CharField(max_length=10, default="")
    tipo_operacao = models.CharField(max_length=20, verbose_name='tipo de operação', null=True, blank=True)
    data_operacao = models.DateField(verbose_name='data da operação')
    qtd = models.IntegerField(verbose_name='quantidade')
    valor_cota = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='valor da cota')
    fonte_recurso = models.CharField(max_length=20, verbose_name='Fonte de recurso', null=True, blank=True)
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Total da Operação')
    mes = models.CharField(max_length=15, verbose_name='mês', null=True, blank=True)
    ano = models.IntegerField(verbose_name='ano', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    def save(self, *args, **kwargs):
        if self.qtd and self.valor_cota:
            self.valor_total = self.qtd * self.valor_cota
        if self.data_operacao:
            self.ano = self.data_operacao.year
            self.mes = self.data_operacao.month
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id_ativo.ticket if self.id_ativo else "Ativo excluído"} - {self.classe}'

####################################### META #############################################
class MetaAtivo(models.Model):
    class Meta:
        verbose_name = "Meta"
        verbose_name_plural = "Meta"
        ordering = ['-ano']

    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_meta", null=True)
    ano = models.IntegerField(verbose_name="Ano", null=True, blank=True)
    classe = models.CharField(max_length=10, default="")
    meta_anual = models.IntegerField(verbose_name="Meta Anual", null=True, blank=True, default=0)
    meta_alcancada = models.IntegerField(verbose_name="Meta anual alcançada", null=True, blank=True)
    meta_geral = models.IntegerField(verbose_name="Meta geral", null=True, blank=True, default=0)
    meta_geral_alcancada = models.IntegerField(verbose_name="Meta geral alcançada", null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    def __str__(self):
        return self.classe

####################################### PLANMETAS #############################################
class PlanMetas(models.Model):
    class Meta:
        verbose_name = "Planejamento das metas"
        verbose_name_plural = "Planejamento das metas"

    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_meta_ativo", null=True)
    id_ativo = models.ForeignKey(Ativos, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ativos")
    classe = models.CharField(max_length=10, default="")
    qtd = models.IntegerField(verbose_name="Quantidade", default=0, blank=True, null=True)
    qtd_calc = models.IntegerField(default=0, blank=True, null=True)
    prov_cota = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='proventos', blank=True, null=True, default=Decimal('0.00'))
    ano = models.IntegerField(verbose_name="Ano", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    def __str__(self):
        return f'{self.id_ativo.ticket if self.id_ativo else "Ativo excluído"} - {self.classe}'

class PlanMetasCalc(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_meta_plan_calc", null=True)
    classe = models.CharField(max_length=10, default="")
    valor_investido = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    saldo = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))

    def __str__(self):
        return self.classe

####################################### PREÇO TETO #############################################
class PrecoTeto(models.Model):
    class Meta:
        verbose_name = "Preço teto"
        verbose_name_plural = "Preço teto"

    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_preco_teto", null=True)
    id_ativo = models.ForeignKey(Ativos, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ativos")
    classe = models.CharField(max_length=10, default="")
    rentabilidade = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Rentabilidade desejada', default=Decimal('6.00'))
    ipca = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='IPCA+', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    def __str__(self):
        return f'{self.id_ativo.ticket if self.id_ativo else "Ativo excluído"} - {self.classe}'

####################################### RENTABILIDADE #############################################
class Rentabilidade(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rentabilidade", null=True)
    id_ativo = models.ForeignKey(Ativos, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ativo')
    rentabilidade = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    ano = models.IntegerField(verbose_name='ano', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')

    def __str__(self):
        return f'{self.id_ativo.ticket if self.id_ativo else "Ativo excluído"} - {self.ano}'

####################################### CORRETORA #############################################
class Corretora(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_corretora", null=True)
    nome_corretora = models.CharField(max_length=255)
    apelido = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, verbose_name='CNPJ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='atualizado em')

    def __str__(self):
        return self.apelido
