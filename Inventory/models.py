from django.db import models
from django.utils import timezone
from Core.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    total_quantity = models.PositiveIntegerField(verbose_name='Quantidade Total')
    available_quantity = models.PositiveIntegerField(verbose_name='Quantidade Disponível')
    location = models.CharField(max_length=100, verbose_name='Localização')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
    
    def __str__(self):
        return f"{self.name} ({self.available_quantity}/{self.total_quantity})"

class Loan(models.Model):
    STATUS_CHOICES = (
        ('active', 'Ativo'),
        ('returned', 'Devolvido'),
        ('late', 'Atrasado'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='loans', verbose_name='Usuário')
    materials = models.ManyToManyField(Material, through='LoanItem', verbose_name='Materiais')
    loan_date = models.DateTimeField(default=timezone.now, verbose_name='Data de Empréstimo')
    expected_return_date = models.DateTimeField(verbose_name='Data Prevista para Devolução')
    return_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de Devolução')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='Status')
    notes = models.TextField(blank=True, verbose_name='Observações')
    
    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
    
    def __str__(self):
        return f"Empréstimo {self.id} - {self.user.username}"
    
    def is_late(self):
        if self.status == 'active' and timezone.now() > self.expected_return_date:
            self.status = 'late'
            self.save()
            return True
        return self.status == 'late'

class LoanItem(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, verbose_name='Empréstimo')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    returned_quantity = models.PositiveIntegerField(default=0, verbose_name='Quantidade Devolvida')
    
    class Meta:
        verbose_name = 'Item de Empréstimo'
        verbose_name_plural = 'Itens de Empréstimo'
    
    def __str__(self):
        return f"{self.material.name} ({self.returned_quantity}/{self.quantity})"