from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time, timedelta
from .models import CustomUser, Disciplina, Horario
from .validators import HorarioValidator


class HorarioValidatorTest(TestCase):
    def setUp(self):
        # Criar usuário de teste (professor)
        self.professor = CustomUser.objects.create_user(
            username='professor_test',
            password='testpass',
            tipo='professor'
        )
        
        # Criar disciplina de teste
        self.disciplina = Disciplina.objects.create(
            nome="Programação Orientada a Objetos",
            curso="Ciência da Computação",
            codigo="POO1001",
            semestre=3
        )
        
        # Obter dia da semana atual
        self.today = timezone.now().date()
        self.current_weekday = self.today.weekday()
        self.dias_semana = [
            'Segunda-feira', 'Terça-feira', 'Quarta-feira', 
            'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
        ]
        self.current_day_name = self.dias_semana[self.current_weekday]
        
        # Criar horário no dia atual, mas no futuro
        current_time = timezone.now().time()
        future_hour = (current_time.hour + 2) % 24  # 2 horas no futuro
        
        self.horario_futuro = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana=self.current_day_name,
            hora_inicio=time(future_hour, 0),
            hora_fim=time(future_hour + 1, 0),
            local="Sala 101"
        )
        
        # Criar horário no dia atual, mas no passado
        past_hour = (current_time.hour - 2) % 24  # 2 horas no passado
        
        self.horario_passado = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana=self.current_day_name,
            hora_inicio=time(past_hour, 0),
            hora_fim=time(past_hour + 1, 0),
            local="Sala 102"
        )

    def test_validate_future_schedule_with_instance(self):
        """Teste de validação de horário futuro usando instância"""
        # Horário futuro deve ser válido
        self.assertTrue(HorarioValidator.validate_future_schedule(horario_instance=self.horario_futuro))
        
        # Horário passado deve ser inválido
        self.assertFalse(HorarioValidator.validate_future_schedule(horario_instance=self.horario_passado))

    def test_validate_future_schedule_with_params(self):
        """Teste de validação de horário futuro usando parâmetros"""
        # Obter próximo dia da semana (amanhã)
        next_weekday = (self.current_weekday + 1) % 7
        next_day_name = self.dias_semana[next_weekday]
        
        # Horário futuro (amanhã) deve ser válido
        self.assertTrue(HorarioValidator.validate_future_schedule(
            dia_semana=next_day_name,
            hora_inicio=time(10, 0),
            hora_fim=time(12, 0)
        ))
        
        # Horário passado (ontem) deve ser inválido
        prev_weekday = (self.current_weekday - 1) % 7
        prev_day_name = self.dias_semana[prev_weekday]
        
        self.assertFalse(HorarioValidator.validate_future_schedule(
            dia_semana=prev_day_name,
            hora_inicio=time(10, 0),
            hora_fim=time(12, 0)
        ))

    def test_validate_schedule_conflict(self):
        """Teste de validação de conflito de horário"""
        # Criar horário sem conflito (diferente dia da semana)
        next_weekday = (self.current_weekday + 1) % 7
        next_day_name = self.dias_semana[next_weekday]
        
        # Não deve haver conflito com horário em outro dia
        self.assertTrue(HorarioValidator.validate_schedule_conflict(
            professor=self.professor,
            dia_semana=next_day_name,
            hora_inicio=time(10, 0),
            hora_fim=time(12, 0)
        ))
        
        # Deve haver conflito com horário no mesmo dia e hora
        self.assertFalse(HorarioValidator.validate_schedule_conflict(
            professor=self.professor,
            dia_semana=self.horario_futuro.dia_semana,
            hora_inicio=self.horario_futuro.hora_inicio,
            hora_fim=self.horario_futuro.hora_fim
        ))
        
        # Não deve haver conflito se excluirmos o próprio horário
        self.assertTrue(HorarioValidator.validate_schedule_conflict(
            professor=self.professor,
            dia_semana=self.horario_futuro.dia_semana,
            hora_inicio=self.horario_futuro.hora_inicio,
            hora_fim=self.horario_futuro.hora_fim,
            exclude_id=self.horario_futuro.id
        ))

    def test_validate_required_fields(self):
        """Teste de validação de campos obrigatórios"""
        # Todos os campos presentes deve ser válido
        self.assertTrue(HorarioValidator.validate_required_fields(
            disciplina=self.disciplina,
            local="Sala 101"
        ))
        
        # Disciplina ausente deve lançar ValidationError
        with self.assertRaises(ValidationError):
            HorarioValidator.validate_required_fields(
                disciplina=None,
                local="Sala 101"
            )
        
        # Local ausente deve lançar ValidationError
        with self.assertRaises(ValidationError):
            HorarioValidator.validate_required_fields(
                disciplina=self.disciplina,
                local=""
            )
        
        # Local com apenas espaços deve lançar ValidationError
        with self.assertRaises(ValidationError):
            HorarioValidator.validate_required_fields(
                disciplina=self.disciplina,
                local="   "
            )
        
        # Ambos ausentes deve lançar ValidationError
        with self.assertRaises(ValidationError):
            HorarioValidator.validate_required_fields(
                disciplina=None,
                local=None
            )