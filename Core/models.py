from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Aluno'),
        ('professor', 'Professor'),
        ('other', 'Outro'),
    )
    
    registration_id = models.CharField(max_length=20, verbose_name='Matrícula')
    user_type = models.CharField(max_length=15, choices=USER_TYPES, default='student', verbose_name='Tipo de Usuário')
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
