from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Q, CheckConstraint
from django.db.models import Q, CheckConstraint
from django.utils import timezone

class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = (
        ("aluno", "Aluno"),
        ("professor", "Professor"),
        ("monitor", "Monitor"),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '            'granted to each of their groups.'
        ),
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="user",
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(tipo__in=["aluno", "professor", "monitor"]),
                name="tipo_usuario_valido",
            )
        ]

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True, default='TEMP0000')  # Temporary default
    semestre = models.IntegerField(default=1)  # Temporary default
    ativo = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['curso']),
            models.Index(fields=['semestre']),
            models.Index(fields=['ativo']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class Horario(models.Model):
    professor_monitor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='horarios')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    local = models.CharField(max_length=100)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['dia_semana']),
            models.Index(fields=['hora_inicio']),
            models.Index(fields=['hora_fim']),
            models.Index(fields=['local']),
            models.Index(fields=['ativo']),
            models.Index(fields=['ultima_atualizacao']),
        ]

    def __str__(self):
        return f"{self.professor_monitor.username} - {self.dia_semana} ({self.hora_inicio}-{self.hora_fim})"

