from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from core.models import CustomUser, Disciplina, Horario
from datetime import time

User = get_user_model()


class CustomUserModelTest(TestCase):
    def setUp(self):
        # Criar usuários de teste
        self.aluno = CustomUser.objects.create_user(
            username='aluno_test',
            password='testpass123',
            email='aluno@test.com',
            tipo='aluno',
            first_name='João',
            last_name='Silva'
        )
        
        self.professor = CustomUser.objects.create_user(
            username='professor_test',
            password='testpass123',
            email='professor@test.com',
            tipo='professor',
            first_name='Maria',
            last_name='Souza'
        )
        
        self.monitor = CustomUser.objects.create_user(
            username='monitor_test',
            password='testpass123',
            email='monitor@test.com',
            tipo='monitor',
            first_name='Pedro',
            last_name='Santos'
        )
    
    def test_user_creation(self):
        """Teste se os usuários são criados corretamente"""
        self.assertEqual(self.aluno.username, 'aluno_test')
        self.assertEqual(self.aluno.email, 'aluno@test.com')
        self.assertEqual(self.aluno.tipo, 'aluno')
        self.assertEqual(self.aluno.get_full_name(), 'João Silva')
        
        self.assertEqual(self.professor.username, 'professor_test')
        self.assertEqual(self.professor.email, 'professor@test.com')
        self.assertEqual(self.professor.tipo, 'professor')
        self.assertEqual(self.professor.get_full_name(), 'Maria Souza')
        
        self.assertEqual(self.monitor.username, 'monitor_test')
        self.assertEqual(self.monitor.email, 'monitor@test.com')
        self.assertEqual(self.monitor.tipo, 'monitor')
        self.assertEqual(self.monitor.get_full_name(), 'Pedro Santos')
    
    def test_user_tipo_choices(self):
        """Teste se o campo tipo aceita apenas os valores permitidos"""
        # Valores válidos já testados no test_user_creation
        
        # Testar valor inválido
        with self.assertRaises(IntegrityError):
            self.aluno.tipo = 'invalid'
            self.aluno.save()
    
    def test_username_uniqueness(self):
        """Teste se o campo username deve ser único"""
        with self.assertRaises(Exception):  # IntegrityError ou ValidationError
            CustomUser.objects.create_user(
                username='aluno_test',  # Username já existente
                password='testpass123',
                email='outro_aluno@test.com',
                tipo='aluno'
            )
    
    def test_filter_by_tipo(self):
        """Teste se é possível filtrar usuários por tipo"""
        alunos = CustomUser.objects.filter(tipo='aluno')
        professores = CustomUser.objects.filter(tipo='professor')
        monitores = CustomUser.objects.filter(tipo='monitor')
        
        self.assertEqual(alunos.count(), 1)
        self.assertEqual(professores.count(), 1)
        self.assertEqual(monitores.count(), 1)
        
        self.assertEqual(alunos.first(), self.aluno)
        self.assertEqual(professores.first(), self.professor)
        self.assertEqual(monitores.first(), self.monitor)
    
    def test_create_superuser(self):
        """Teste se é possível criar um superusuário"""
        admin = CustomUser.objects.create_superuser(
            username='admin_test',
            password='adminpass123',
            email='admin@test.com',
            tipo='professor' # Adicionar um tipo válido para passar na CheckConstraint
        )
        
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_active)


class HorarioModelTest(TestCase):
    def setUp(self):
        # Criar usuário de teste (professor)
        self.professor = CustomUser.objects.create_user(
            username='professor_test',
            password='testpass123',
            tipo='professor'
        )
        
        # Criar disciplina de teste
        self.disciplina = Disciplina.objects.create(
            nome="Programação Orientada a Objetos",
            curso="Ciência da Computação",
            codigo="POO1001",
            semestre=3
        )
        
        # Criar horário de teste
        self.horario = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana="Segunda-feira",
            hora_inicio=time(14, 0),
            hora_fim=time(16, 0),
            local="Sala 101"
        )
    
    def test_horario_creation(self):
        """Teste se um horário é criado corretamente"""
        self.assertEqual(self.horario.professor_monitor, self.professor)
        self.assertEqual(self.horario.disciplina, self.disciplina)
        self.assertEqual(self.horario.dia_semana, "Segunda-feira")
        self.assertEqual(self.horario.hora_inicio, time(14, 0))
        self.assertEqual(self.horario.hora_fim, time(16, 0))
        self.assertEqual(self.horario.local, "Sala 101")
        self.assertTrue(self.horario.ativo)  # Default value should be True
        self.assertIsNotNone(self.horario.ultima_atualizacao)
        self.assertIsNotNone(self.horario.data_criacao)
    
    def test_horario_str_representation(self):
        """Teste a representação em string de um horário"""
        expected_str = f"{self.professor.username} - Segunda-feira (14:00:00-16:00:00)"
        self.assertEqual(str(self.horario), expected_str)
    
    def test_horario_relationships(self):
        """Teste os relacionamentos de um horário"""
        # Testar relacionamento com professor
        self.assertIn(self.horario, self.professor.horarios.all())
        
        # Testar relacionamento com disciplina
        self.assertIn(self.horario, self.disciplina.horarios.all())
    
    def test_horario_update(self):
        """Teste se um horário pode ser atualizado"""
        # Atualizar horário
        self.horario.local = "Sala 102"
        self.horario.dia_semana = "Terça-feira"
        self.horario.save()
        
        # Verificar se foi atualizado
        self.horario.refresh_from_db()
        self.assertEqual(self.horario.local, "Sala 102")
        self.assertEqual(self.horario.dia_semana, "Terça-feira")
    
    def test_horario_filter_by_dia_semana(self):
        """Teste se é possível filtrar horários por dia da semana"""
        # Criar outro horário em outro dia
        Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana="Quarta-feira",
            hora_inicio=time(10, 0),
            hora_fim=time(12, 0),
            local="Sala 103"
        )
        
        # Filtrar por dia da semana
        segunda = Horario.objects.filter(dia_semana="Segunda-feira")
        quarta = Horario.objects.filter(dia_semana="Quarta-feira")
        
        self.assertEqual(segunda.count(), 1)
        self.assertEqual(quarta.count(), 1)
        self.assertEqual(segunda.first(), self.horario)
    
    def test_horario_filter_by_disciplina(self):
        """Teste se é possível filtrar horários por disciplina"""
        # Criar outra disciplina
        outra_disciplina = Disciplina.objects.create(
            nome="Cálculo I",
            curso="Engenharia",
            codigo="CAL1001",
            semestre=1
        )
        
        # Criar horário para outra disciplina
        Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=outra_disciplina,
            dia_semana="Quinta-feira",
            hora_inicio=time(8, 0),
            hora_fim=time(10, 0),
            local="Sala 104"
        )
        
        # Filtrar por disciplina
        horarios_poo = Horario.objects.filter(disciplina=self.disciplina)
        horarios_cal = Horario.objects.filter(disciplina=outra_disciplina)
        
        self.assertEqual(horarios_poo.count(), 1)
        self.assertEqual(horarios_cal.count(), 1)
        self.assertEqual(horarios_poo.first(), self.horario)
    
    def test_horario_filter_by_professor(self):
        """Teste se é possível filtrar horários por professor"""
        # Criar outro professor
        outro_professor = CustomUser.objects.create_user(
            username='outro_professor',
            password='testpass123',
            tipo='professor'
        )
        
        # Criar horário para outro professor
        Horario.objects.create(
            professor_monitor=outro_professor,
            disciplina=self.disciplina,
            dia_semana="Sexta-feira",
            hora_inicio=time(14, 0),
            hora_fim=time(16, 0),
            local="Sala 105"
        )
        
        # Filtrar por professor
        horarios_prof1 = Horario.objects.filter(professor_monitor=self.professor)
        horarios_prof2 = Horario.objects.filter(professor_monitor=outro_professor)
        
        self.assertEqual(horarios_prof1.count(), 1)
        self.assertEqual(horarios_prof2.count(), 1)
        self.assertEqual(horarios_prof1.first(), self.horario)