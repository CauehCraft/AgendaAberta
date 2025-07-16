import django_filters
from .models import Horario, Disciplina


class HorarioFilter(django_filters.FilterSet):
    """
    Filtro avançado para horários, permitindo filtrar por diversos critérios.
    """
    curso = django_filters.CharFilter(field_name='disciplina__curso', lookup_expr='icontains')
    disciplina = django_filters.ModelChoiceFilter(queryset=Disciplina.objects.all())
    professor = django_filters.CharFilter(field_name='professor_monitor__username', lookup_expr='icontains')
    professor_nome = django_filters.CharFilter(method='filter_professor_nome')
    dia_semana = django_filters.ChoiceFilter(choices=[
        ('Segunda-feira', 'Segunda-feira'),
        ('Terça-feira', 'Terça-feira'),
        ('Quarta-feira', 'Quarta-feira'),
        ('Quinta-feira', 'Quinta-feira'),
        ('Sexta-feira', 'Sexta-feira'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ])
    periodo = django_filters.CharFilter(method='filter_periodo')
    
    class Meta:
        model = Horario
        fields = ['curso', 'disciplina', 'professor', 'professor_nome', 'dia_semana', 'periodo']
    
    def filter_periodo(self, queryset, name, value):
        """
        Filtra horários por período do dia (manhã, tarde, noite).
        """
        if value.lower() == 'manha':
            return queryset.filter(hora_inicio__lt='12:00')
        elif value.lower() == 'tarde':
            return queryset.filter(hora_inicio__gte='12:00', hora_inicio__lt='18:00')
        elif value.lower() == 'noite':
            return queryset.filter(hora_inicio__gte='18:00')
        return queryset
    
    def filter_professor_nome(self, queryset, name, value):
        """
        Filtra horários pelo nome do professor (first_name ou last_name).
        """
        return queryset.filter(
            professor_monitor__first_name__icontains=value
        ) | queryset.filter(
            professor_monitor__last_name__icontains=value
        )