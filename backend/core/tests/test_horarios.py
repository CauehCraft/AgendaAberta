
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import CustomUser, Disciplina, Horario

class HorarioViewSetTests(APITestCase):
    def setUp(self):
        self.professor = CustomUser.objects.create_user(username='professor', password='password', tipo='professor')
        self.aluno = CustomUser.objects.create_user(username='aluno', password='password', tipo='aluno')
        self.disciplina = Disciplina.objects.create(nome='Test Discipline', curso='Test Course', codigo='TEST001')
        
        refresh = RefreshToken.for_user(self.professor)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_horario(self):
        url = reverse('horario-list')
        data = {
            'disciplina': self.disciplina.id,
            'dia_semana': 'segunda',
            'hora_inicio': '10:00',
            'hora_fim': '11:00',
            'local': 'Sala 101',
            'professor_monitor': self.professor.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Horario.objects.count(), 1)
        self.assertEqual(Horario.objects.get().local, 'Sala 101')

    def test_create_horario_conflict(self):
        Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana='segunda',
            hora_inicio='10:00',
            hora_fim='11:00',
            local='Sala 101'
        )
        url = reverse('horario-list')
        data = {
            'disciplina': self.disciplina.id,
            'dia_semana': 'segunda',
            'hora_inicio': '10:30',
            'hora_fim': '11:30',
            'local': 'Sala 102',
            'professor_monitor': self.professor.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_horarios(self):
        Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana='terca',
            hora_inicio='14:00',
            hora_fim='15:00',
            local='Sala 103'
        )
        url = reverse('horario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_horario(self):
        horario = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana='quarta',
            hora_inicio='08:00',
            hora_fim='09:00',
            local='Sala 104'
        )
        url = reverse('horario-detail', kwargs={'pk': horario.pk})
        data = {'local': 'Sala 202'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        horario.refresh_from_db()
        self.assertEqual(horario.local, 'Sala 202')

    def test_delete_horario(self):
        horario = Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana='quinta',
            hora_inicio='16:00',
            hora_fim='17:00',
            local='Sala 105'
        )
        url = reverse('horario-detail', kwargs={'pk': horario.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Horario.objects.count(), 0)

    def test_public_horario_list(self):
        Horario.objects.create(
            professor_monitor=self.professor,
            disciplina=self.disciplina,
            dia_semana='sexta',
            hora_inicio='11:00',
            hora_fim='12:00',
            local='Sala 106'
        )
        self.client.credentials() # Clear credentials
        url = reverse('horario-publico-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
