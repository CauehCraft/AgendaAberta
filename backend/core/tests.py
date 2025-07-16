from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Disciplina, CustomUser


class DisciplinaModelTest(TestCase):
    def setUp(self):
        # Create a test discipline
        self.disciplina = Disciplina.objects.create(
            nome="Programação Orientada a Objetos",
            curso="Ciência da Computação",
            codigo="POO1001",
            semestre=3
        )

    def test_disciplina_creation(self):
        """Test that a discipline can be created with all required fields"""
        self.assertEqual(self.disciplina.nome, "Programação Orientada a Objetos")
        self.assertEqual(self.disciplina.curso, "Ciência da Computação")
        self.assertEqual(self.disciplina.codigo, "POO1001")
        self.assertEqual(self.disciplina.semestre, 3)
        self.assertTrue(self.disciplina.ativo)  # Default value should be True

    def test_disciplina_str_representation(self):
        """Test the string representation of a discipline"""
        self.assertEqual(str(self.disciplina), "POO1001 - Programação Orientada a Objetos")

    def test_codigo_uniqueness(self):
        """Test that the codigo field must be unique"""
        with self.assertRaises(IntegrityError):
            Disciplina.objects.create(
                nome="Outra Disciplina",
                curso="Outro Curso",
                codigo="POO1001",  # Same code as existing discipline
                semestre=2
            )

    def test_filter_by_semestre(self):
        """Test filtering disciplines by semester"""
        # Create another discipline with a different semester
        Disciplina.objects.create(
            nome="Cálculo I",
            curso="Ciência da Computação",
            codigo="CAL1001",
            semestre=1
        )
        
        # Filter by semester
        semestre_3 = Disciplina.objects.filter(semestre=3)
        semestre_1 = Disciplina.objects.filter(semestre=1)
        
        self.assertEqual(semestre_3.count(), 1)
        self.assertEqual(semestre_1.count(), 1)
        self.assertEqual(semestre_3.first().nome, "Programação Orientada a Objetos")
        self.assertEqual(semestre_1.first().nome, "Cálculo I")

    def test_filter_by_ativo(self):
        """Test filtering disciplines by active status"""
        # Create an inactive discipline
        Disciplina.objects.create(
            nome="Disciplina Inativa",
            curso="Curso Antigo",
            codigo="DIS1002",
            semestre=2,
            ativo=False
        )
        
        # Filter by active status
        ativas = Disciplina.objects.filter(ativo=True)
        inativas = Disciplina.objects.filter(ativo=False)
        
        self.assertEqual(ativas.count(), 1)
        self.assertEqual(inativas.count(), 1)
        self.assertEqual(ativas.first().nome, "Programação Orientada a Objetos")
        self.assertEqual(inativas.first().nome, "Disciplina Inativa")

class DisciplinaAPITest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            tipo='aluno'
        )
        
        # Create test disciplines
        self.disciplina1 = Disciplina.objects.create(
            nome="Programação Orientada a Objetos",
            curso="Ciência da Computação",
            codigo="POO1001",
            semestre=3
        )
        
        self.disciplina2 = Disciplina.objects.create(
            nome="Cálculo I",
            curso="Engenharia",
            codigo="CAL1001",
            semestre=1
        )
        
        self.disciplina3 = Disciplina.objects.create(
            nome="Estruturas de Dados",
            curso="Ciência da Computação",
            codigo="EDD1001",
            semestre=4,
            ativo=False
        )

    def test_list_disciplinas_authenticated(self):
        """Test that authenticated users can list disciplines"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/disciplinas/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_disciplinas_unauthenticated(self):
        """Test that unauthenticated users cannot access disciplines"""
        response = self.client.get('/api/disciplinas/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_by_curso(self):
        """Test filtering disciplines by course"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/disciplinas/?curso=Ciência')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # POO and EDD

    def test_filter_by_semestre(self):
        """Test filtering disciplines by semester"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/disciplinas/?semestre=1')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Cálculo I")

    def test_filter_by_ativo(self):
        """Test filtering disciplines by active status"""
        self.client.force_authenticate(user=self.user)
        
        # Test active disciplines
        response = self.client.get('/api/disciplinas/?ativo=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Test inactive disciplines
        response = self.client.get('/api/disciplinas/?ativo=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Estruturas de Dados")

    def test_search_disciplinas(self):
        """Test searching disciplines by name or code"""
        self.client.force_authenticate(user=self.user)
        
        # Search by name
        response = self.client.get('/api/disciplinas/?search=POO')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['codigo'], "POO1001")
        
        # Search by code
        response = self.client.get('/api/disciplinas/?search=CAL1001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Cálculo I")

    def test_create_disciplina(self):
        """Test creating a new discipline"""
        self.client.force_authenticate(user=self.user)
        data = {
            'nome': 'Algoritmos',
            'curso': 'Ciência da Computação',
            'codigo': 'ALG1001',
            'semestre': 2,
            'ativo': True  # Explicitly set the value
        }
        
        response = self.client.post('/api/disciplinas/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Disciplina.objects.count(), 4)
        
        # Verify the created discipline
        disciplina = Disciplina.objects.get(codigo='ALG1001')
        self.assertEqual(disciplina.nome, 'Algoritmos')
        self.assertTrue(disciplina.ativo)

    def test_update_disciplina(self):
        """Test updating an existing discipline"""
        self.client.force_authenticate(user=self.user)
        data = {
            'nome': 'POO Avançado',
            'curso': 'Ciência da Computação',
            'codigo': 'POO1001',
            'semestre': 4,
            'ativo': True
        }
        
        response = self.client.put(f'/api/disciplinas/{self.disciplina1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the update
        self.disciplina1.refresh_from_db()
        self.assertEqual(self.disciplina1.nome, 'POO Avançado')
        self.assertEqual(self.disciplina1.semestre, 4)

    def test_delete_disciplina(self):
        """Test deleting a discipline"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/disciplinas/{self.disciplina1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Disciplina.objects.count(), 2)
        self.assertFalse(Disciplina.objects.filter(id=self.disciplina1.id).exists())


from django.utils import timezone
from datetime import date, time
from .models import Agendamento, Horario


class AgendamentoModelTest(TestCase):
    def setUp(self):
        # Create test users
        self.aluno = CustomUser.objects.create_user(
            username='aluno_test',
            password='testpass',
            tipo='aluno'
        )
        
        self.professor = CustomUser.objects.create_user(
            username='professor_test',
            password='testpass',
            tipo='professor'
        )
        
        # Create test discipline
        self.disciplina = Disciplina.objects.create(
            nome="Programação Orientada a Objetos",
            curso="Ciência da Computação",
            codigo="POO1001",
            semestre=3
        )
        
        # Create test schedule
        self.horario = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana="Segunda-feira",
            hora_inicio=time(14, 0),
            hora_fim=time(16, 0),
            local="Sala 101"
        )

    def test_agendamento_creation_with_defaults(self):
        """Test that an agendamento can be created with default values"""
        agendamento = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario
        )
        
        self.assertEqual(agendamento.aluno, self.aluno)
        self.assertEqual(agendamento.horario, self.horario)
        self.assertEqual(agendamento.status, 'agendado')  # Default status
        self.assertIsNone(agendamento.observacoes)  # Default null
        self.assertIsNotNone(agendamento.data_criacao)  # Auto-generated
        self.assertIsNotNone(agendamento.data_atualizacao)  # Auto-generated
        self.assertEqual(agendamento.data.date(), timezone.now().date())  # Default to today

    def test_agendamento_creation_with_all_fields(self):
        """Test creating an agendamento with all fields specified"""
        test_date = date(2024, 12, 15)
        agendamento = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            data=test_date,
            status='confirmado',
            observacoes='Revisão para prova final'
        )
        
        self.assertEqual(agendamento.data, test_date)
        self.assertEqual(agendamento.status, 'confirmado')
        self.assertEqual(agendamento.observacoes, 'Revisão para prova final')

    def test_agendamento_status_choices(self):
        """Test all valid status choices"""
        valid_statuses = ['agendado', 'confirmado', 'cancelado', 'realizado']
        
        for status_choice in valid_statuses:
            agendamento = Agendamento.objects.create(
                aluno=self.aluno,
                horario=self.horario,
                status=status_choice
            )
            self.assertEqual(agendamento.status, status_choice)

    def test_agendamento_str_representation(self):
        """Test the string representation of an agendamento"""
        agendamento = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            status='confirmado'
        )
        
        expected_str = f"Agendamento de {self.aluno.username} com {self.professor.username} - confirmado"
        self.assertEqual(str(agendamento), expected_str)

    def test_agendamento_update_timestamps(self):
        """Test that data_atualizacao is updated when the model is saved"""
        agendamento = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario
        )
        
        original_update_time = agendamento.data_atualizacao
        
        # Wait a moment and update
        import time
        time.sleep(0.01)
        
        agendamento.status = 'confirmado'
        agendamento.save()
        
        self.assertGreater(agendamento.data_atualizacao, original_update_time)

    def test_agendamento_relationships(self):
        """Test the foreign key relationships"""
        agendamento = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario
        )
        
        # Test reverse relationships
        self.assertIn(agendamento, self.aluno.agendamentos.all())
        self.assertIn(agendamento, self.horario.agendamentos.all())

    def test_agendamento_cascade_delete(self):
        """Test that agendamentos are deleted when related objects are deleted"""
        agendamento = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario
        )
        
        agendamento_id = agendamento.id
        
        # Delete the aluno - should cascade delete the agendamento
        self.aluno.delete()
        
        self.assertFalse(Agendamento.objects.filter(id=agendamento_id).exists())

    def test_agendamento_observacoes_optional(self):
        """Test that observacoes field is optional"""
        # Test with empty string
        agendamento1 = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            observacoes=""
        )
        self.assertEqual(agendamento1.observacoes, "")
        
        # Test with None
        agendamento2 = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            observacoes=None
        )
        self.assertIsNone(agendamento2.observacoes)

    def test_filter_by_status(self):
        """Test filtering agendamentos by status"""
        # Create agendamentos with different statuses
        Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            status='agendado'
        )
        
        Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            status='confirmado'
        )
        
        Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            status='cancelado'
        )
        
        # Test filtering
        agendados = Agendamento.objects.filter(status='agendado')
        confirmados = Agendamento.objects.filter(status='confirmado')
        cancelados = Agendamento.objects.filter(status='cancelado')
        
        self.assertEqual(agendados.count(), 1)
        self.assertEqual(confirmados.count(), 1)
        self.assertEqual(cancelados.count(), 1)

    def test_filter_by_date_range(self):
        """Test filtering agendamentos by date range"""
        today = timezone.now().date()
        tomorrow = today + timezone.timedelta(days=1)
        
        # Create agendamentos for different dates
        Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            data=today
        )
        
        Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            data=tomorrow
        )
        
        # Test filtering by date
        today_agendamentos = Agendamento.objects.filter(data=today)
        tomorrow_agendamentos = Agendamento.objects.filter(data=tomorrow)
        
        self.assertEqual(today_agendamentos.count(), 1)
        self.assertEqual(tomorrow_agendamentos.count(), 1)


class AgendamentoAPITest(APITestCase):
    def setUp(self):
        # Create test users
        self.aluno = CustomUser.objects.create_user(
            username='aluno_test',
            password='testpass',
            tipo='aluno'
        )
        
        self.professor = CustomUser.objects.create_user(
            username='professor_test',
            password='testpass',
            tipo='professor'
        )
        
        # Create test discipline
        self.disciplina = Disciplina.objects.create(
            nome="Programação Orientada a Objetos",
            curso="Ciência da Computação",
            codigo="POO1001",
            semestre=3
        )
        
        # Create test schedule
        self.horario = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana="Segunda-feira",
            hora_inicio=time(14, 0),
            hora_fim=time(16, 0),
            local="Sala 101"
        )
        
        # Create test agendamento
        self.agendamento = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            status='agendado',
            observacoes='Dúvidas sobre herança'
        )

    def test_list_agendamentos_authenticated(self):
        """Test that authenticated users can list agendamentos"""
        self.client.force_authenticate(user=self.aluno)
        response = self.client.get('/api/agendamentos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_agendamento(self):
        """Test creating a new agendamento"""
        self.client.force_authenticate(user=self.aluno)
        data = {
            'aluno': self.aluno.id,
            'horario': self.horario.id,
            'data': '2024-12-20',
            'status': 'agendado',
            'observacoes': 'Revisão para prova'
        }
        
        response = self.client.post('/api/agendamentos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Agendamento.objects.count(), 2)

    def test_update_agendamento_status(self):
        """Test updating agendamento status"""
        self.client.force_authenticate(user=self.professor)
        data = {
            'aluno': self.aluno.id,
            'horario': self.horario.id,
            'data': str(self.agendamento.data),
            'status': 'confirmado',
            'observacoes': self.agendamento.observacoes
        }
        
        response = self.client.put(f'/api/agendamentos/{self.agendamento.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the update
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, 'confirmado')

    def test_filter_agendamentos_by_status(self):
        """Test filtering agendamentos by status"""
        # Create additional agendamento with different status
        Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            status='confirmado'
        )
        
        self.client.force_authenticate(user=self.aluno)
        
        # Filter by status
        response = self.client.get('/api/agendamentos/?status=agendado')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'agendado')

    def test_filter_agendamentos_by_date(self):
        """Test filtering agendamentos by date"""
        self.client.force_authenticate(user=self.aluno)
        
        today = timezone.now().date()
        response = self.client.get(f'/api/agendamentos/?data={today}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)