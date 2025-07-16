from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import time, date
from .models import CustomUser, Disciplina, Horario, Agendamento
from .serializers import AgendamentoSerializer


class AgendamentoVisualizacaoTest(TestCase):
    def setUp(self):
        # Criar cliente API
        self.client = APIClient()
        
        # Criar usuários de teste
        self.aluno = CustomUser.objects.create_user(
            username='aluno_test',
            password='testpass123',
            tipo='aluno'
        )
        
        self.professor = CustomUser.objects.create_user(
            username='professor_test',
            password='testpass123',
            tipo='professor',
            first_name='João',
            last_name='Silva'
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
        
        # Criar agendamento de teste
        self.agendamento = Agendamento.objects.create(
            aluno=self.aluno,
            horario=self.horario,
            data=date.today(),
            status='agendado',
            observacoes='Dúvidas sobre herança'
        )
        
        # Autenticar cliente como aluno
        self.client.force_authenticate(user=self.aluno)
    
    def test_mensagem_visualizacao_no_serializer(self):
        """Teste se a mensagem de visualização está presente no serializer"""
        serializer = AgendamentoSerializer(instance=self.agendamento)
        self.assertIn('mensagem_visualizacao', serializer.data)
        self.assertEqual(
            serializer.data['mensagem_visualizacao'],
            "Este sistema é principalmente para visualização de horários disponíveis, não para agendamento."
        )
    
    def test_horario_detalhes_no_serializer(self):
        """Teste se os detalhes do horário estão presentes no serializer"""
        serializer = AgendamentoSerializer(instance=self.agendamento)
        self.assertIn('horario_detalhes', serializer.data)
        self.assertEqual(serializer.data['horario_detalhes']['dia_semana'], "Segunda-feira")
        self.assertEqual(serializer.data['horario_detalhes']['local'], "Sala 101")
        self.assertEqual(serializer.data['horario_detalhes']['disciplina'], "Programação Orientada a Objetos")
    
    def test_mensagem_visualizacao_na_api(self):
        """Teste se a mensagem de visualização está presente na resposta da API"""
        url = reverse('agendamento-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(
            response.data['message'],
            "Este sistema é principalmente para visualização de horários disponíveis, não para agendamento."
        )
    
    def test_aluno_nao_pode_criar_agendamento_para_outro_aluno(self):
        """Teste se um aluno não pode criar agendamento para outro aluno"""
        url = reverse('agendamento-list')
        data = {
            'aluno': self.professor.id,  # Tentando criar para outro usuário
            'horario': self.horario.id,
            'data': '2025-12-20',
            'status': 'agendado',
            'observacoes': 'Tentativa inválida'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o agendamento foi criado para o aluno autenticado, não para o professor
        agendamento = Agendamento.objects.get(id=response.data['id'])
        self.assertEqual(agendamento.aluno, self.aluno)
        self.assertNotEqual(agendamento.aluno, self.professor)