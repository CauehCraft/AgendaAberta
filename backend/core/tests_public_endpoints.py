from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import time
from .models import CustomUser, Disciplina, Horario


class HorarioPublicViewSetTest(TestCase):
    def setUp(self):
        # Criar cliente API
        self.client = APIClient()
        
        # Criar usuário de teste (professor)
        self.professor = CustomUser.objects.create_user(
            username='professor_test',
            password='testpass123',
            tipo='professor',
            first_name='João',
            last_name='Silva'
        )
        
        # Criar disciplinas de teste
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
        
        # Criar horários de teste
        self.horario1 = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina1,
            dia_semana="Segunda-feira",
            hora_inicio=time(14, 0),
            hora_fim=time(16, 0),
            local="Sala 101"
        )
        
        self.horario2 = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina2,
            dia_semana="Terça-feira",
            hora_inicio=time(10, 0),
            hora_fim=time(12, 0),
            local="Sala 102"
        )
    
    def test_list_horarios_publicos_without_auth(self):
        """Teste se usuários não autenticados podem listar horários públicos"""
        url = reverse('horario-publico-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_message_in_response(self):
        """Teste se a mensagem informativa está presente na resposta"""
        url = reverse('horario-publico-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(
            response.data['message'], 
            "Este sistema é apenas para visualização de horários disponíveis, não para agendamento."
        )
    
    def test_retrieve_horario_publico_without_auth(self):
        """Teste se usuários não autenticados podem visualizar um horário específico"""
        url = reverse('horario-publico-detail', args=[self.horario1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.horario1.id)
        self.assertIn('message', response.data)
    
    def test_filter_by_curso(self):
        """Teste se é possível filtrar horários por curso"""
        url = reverse('horario-publico-list')
        response = self.client.get(url, {'curso': 'Ciência'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['disciplina_nome'], "Programação Orientada a Objetos")
    
    def test_filter_by_disciplina(self):
        """Teste se é possível filtrar horários por disciplina"""
        url = reverse('horario-publico-list')
        response = self.client.get(url, {'disciplina': self.disciplina1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['disciplina_nome'], "Programação Orientada a Objetos")
    
    def test_filter_by_dia_semana(self):
        """Teste se é possível filtrar horários por dia da semana"""
        url = reverse('horario-publico-list')
        response = self.client.get(url, {'dia_semana': 'Segunda-feira'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['dia_semana'], "Segunda-feira")
    
    def test_filter_by_professor_nome(self):
        """Teste se é possível filtrar horários pelo nome do professor"""
        url = reverse('horario-publico-list')
        response = self.client.get(url, {'professor_nome': 'João'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_by_periodo(self):
        """Teste se é possível filtrar horários por período"""
        url = reverse('horario-publico-list')
        response = self.client.get(url, {'periodo': 'manha'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['hora_inicio'], '10:00:00')
    
    def test_search_by_local(self):
        """Teste se é possível buscar horários por local"""
        url = reverse('horario-publico-list')
        response = self.client.get(url, {'search': '101'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['local'], "Sala 101")
    
    def test_write_operations_not_allowed(self):
        """Teste se operações de escrita não são permitidas"""
        # Teste POST (criar)
        url = reverse('horario-publico-list')
        data = {
            'professor_monitor': self.professor.id,
            'disciplina': self.disciplina1.id,
            'dia_semana': 'Quarta-feira',
            'hora_inicio': '08:00:00',
            'hora_fim': '10:00:00',
            'local': 'Sala 103'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Teste PUT (atualizar)
        url = reverse('horario-publico-detail', args=[self.horario1.id])
        data = {'local': 'Sala Nova'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Teste DELETE (excluir)
        url = reverse('horario-publico-detail', args=[self.horario1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)