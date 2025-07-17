from django.contrib import admin
from .models import CustomUser, Disciplina, Horario

admin.site.register(CustomUser)

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'curso', 'semestre', 'ativo')
    list_filter = ('curso', 'semestre', 'ativo')
    search_fields = ('nome', 'codigo', 'curso')
    ordering = ('codigo', 'nome')

admin.site.register(Horario)
