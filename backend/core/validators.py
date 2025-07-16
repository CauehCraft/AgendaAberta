from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Horario


class HorarioValidator:
    @staticmethod
    def validate_future_schedule(horario_instance=None, dia_semana=None, hora_inicio=None, hora_fim=None):
        """
        Valida se o horário é futuro para edição.
        
        Pode ser usado de duas formas:
        1. Com uma instância de Horario: validate_future_schedule(horario_instance=horario)
        2. Com dados separados: validate_future_schedule(dia_semana='Segunda-feira', hora_inicio=time(14, 0), hora_fim=time(16, 0))
        
        Retorna True se o horário é futuro ou está no dia atual mas ainda não passou.
        Lança ValidationError se o horário já passou.
        """
        today = timezone.now().date()
        current_time = timezone.now().time()
        
        # Mapear dias da semana para números (0 = Segunda, 6 = Domingo)
        dias_semana = {
            'Segunda-feira': 0,
            'Terça-feira': 1,
            'Quarta-feira': 2,
            'Quinta-feira': 3,
            'Sexta-feira': 4,
            'Sábado': 5,
            'Domingo': 6
        }
        
        # Se foi passada uma instância de Horario
        if horario_instance:
            dia_semana = horario_instance.dia_semana
            hora_inicio = horario_instance.hora_inicio
            hora_fim = horario_instance.hora_fim
        
        # Verificar se os dados necessários foram fornecidos
        if not dia_semana or not hora_inicio or not hora_fim:
            raise ValueError("Dados insuficientes para validação de horário futuro")
        
        # Obter o dia da semana atual (0 = Segunda, 6 = Domingo)
        current_weekday = today.weekday()
        
        # Obter o dia da semana do horário
        if dia_semana not in dias_semana:
            raise ValueError(f"Dia da semana inválido: {dia_semana}")
        
        horario_weekday = dias_semana[dia_semana]
        
        # Se o dia da semana já passou esta semana
        if horario_weekday < current_weekday:
            return False
        
        # Se é o dia atual, verificar se o horário já passou
        if horario_weekday == current_weekday and hora_fim <= current_time:
            return False
        
        return True
    
    @staticmethod
    def validate_schedule_conflict(professor, dia_semana, hora_inicio, hora_fim, exclude_id=None):
        """
        Valida se há conflitos de horário para um professor/monitor.
        
        Args:
            professor: Instância de CustomUser (professor ou monitor)
            dia_semana: Dia da semana do horário
            hora_inicio: Hora de início
            hora_fim: Hora de fim
            exclude_id: ID de um horário a ser excluído da verificação (útil para edição)
            
        Retorna:
            True se não há conflitos, False se há conflitos
        """
        # Verificar se há horários que se sobrepõem
        conflicts = Horario.objects.filter(
            professor_monitor=professor,
            dia_semana=dia_semana,
            hora_inicio__lt=hora_fim,
            hora_fim__gt=hora_inicio
        )
        
        # Excluir o próprio horário da verificação (para edição)
        if exclude_id:
            conflicts = conflicts.exclude(id=exclude_id)
        
        return not conflicts.exists()
    
    @staticmethod
    def validate_required_fields(disciplina=None, local=None):
        """
        Valida se os campos obrigatórios estão presentes.
        
        Args:
            disciplina: Instância de Disciplina ou None
            local: String do local ou None
            
        Retorna:
            True se todos os campos obrigatórios estão presentes
            
        Raises:
            ValidationError: Se algum campo obrigatório está ausente
        """
        errors = {}
        
        if not disciplina:
            errors['disciplina'] = "O campo disciplina é obrigatório."
        
        if not local or not local.strip():
            errors['local'] = "O campo local/sala é obrigatório."
        
        if errors:
            raise ValidationError(errors)
        
        return True