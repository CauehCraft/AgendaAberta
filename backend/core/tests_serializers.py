from django.test import TestCase
from django.utils import timezone
from datetime import time
from .models import CustomUser, Disciplina, Horario
from .serializers import (
    HorarioSerializer, HorarioDetailSerializer, 
    HorarioPublicSerializer, UserBasicSerializer
)


class UserBasicSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'professor_test',
            'password': 'testpass123',
            'tipo': 'professor',
            'first_name': 'João',
            'last_name': 'Silva'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.serializer = UserBasicSerializer(instance=self.user)
    
    def test_contains_expected_fields(self):
        """Teste se o serializer contém os campos esperados"""
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'username', 'tipo', 'nome_completo'])
    
    def test_nome_completo_field(self):
        """Teste se o campo nome_completo está correto"""
        data = self.serializer.data
        self.assertEqual(data['nome_completo'], 'João Silva')
    
    def test_nome_completo_field_without_name(self):
        """Teste se o campo nome_completo retorna username quando não há nome"""
        user = CustomUser.objects.create_user(
            username='aluno_test',
            password='testpass123',
            tipo='aluno'
        )
        serializer = UserBasicSerializer(instance=user)
        self.assertEqual(serializer.data['nome_completo'], 'aluno_test')


class HorarioDetailSerializerTest(TestCase):
    def setUp(self):
        # Criar usuário de teste (professor)
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
        
        self.serializer = HorarioDetailSerializer(instance=self.horario)
    
    def test_contains_expected_fields(self):
        """Teste se o serializer contém os campos esperados"""
        data = self.serializer.data
        expected_fields = [
            'id', 'professor_monitor', 'disciplina', 'dia_semana', 
            'hora_inicio', 'hora_fim', 'local', 'ultima_atualizacao',
            'data_criacao', 'ativo', 'tempo_desde_atualizacao'
        ]
        self.assertCountEqual(data.keys(), expected_fields)
    
    def test_disciplina_field_is_nested(self):
        """Teste se o campo disciplina é aninhado"""
        data = self.serializer.data
        self.assertIsInstance(data['disciplina'], dict)
        self.assertEqual(data['disciplina']['nome'], "Programação Orientada a Objetos")
    
    def test_professor_monitor_field_is_nested(self):
        """Teste se o campo professor_monitor é aninhado"""
        data = self.serializer.data
        self.assertIsInstance(data['professor_monitor'], dict)
        self.assertEqual(data['professor_monitor']['nome_completo'], "João Silva")
    
    def test_tempo_desde_atualizacao_field(self):
        """Teste se o campo tempo_desde_atualizacao está presente"""
        data = self.serializer.data
        self.assertIn('tempo_desde_atualizacao', data)
        # Como o horário acabou de ser criado, deve ser "Agora mesmo"
        self.assertEqual(data['tempo_desde_atualizacao'], "Agora mesmo")


class HorarioPublicSerializerTest(TestCase):
    def setUp(self):
        # Criar usuário de teste (professor)
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
        
        self.serializer = HorarioPublicSerializer(instance=self.horario)
    
    def test_contains_expected_fields(self):
        """Teste se o serializer contém os campos esperados"""
        data = self.serializer.data
        expected_fields = [
            'id', 'dia_semana', 'hora_inicio', 'hora_fim', 'local',
            'disciplina_nome', 'disciplina_codigo', 'curso',
            'professor_nome', 'ultima_atualizacao_formatada'
        ]
        self.assertCountEqual(data.keys(), expected_fields)
    
    def test_sensitive_fields_are_omitted(self):
        """Teste se campos sensíveis são omitidos"""
        data = self.serializer.data
        self.assertNotIn('professor_monitor', data)
        self.assertNotIn('disciplina', data)
    
    def test_professor_nome_field(self):
        """Teste se o campo professor_nome está correto"""
        data = self.serializer.data
        self.assertEqual(data['professor_nome'], "João Silva")
    
    def test_disciplina_fields(self):
        """Teste se os campos de disciplina estão corretos"""
        data = self.serializer.data
        self.assertEqual(data['disciplina_nome'], "Programação Orientada a Objetos")
        self.assertEqual(data['disciplina_codigo'], "POO1001")
        self.assertEqual(data['curso'], "Ciência da Computação")
    
    def test_ultima_atualizacao_formatada_field(self):
        """Teste se o campo ultima_atualizacao_formatada está presente"""
        data = self.serializer.data
        self.assertIn('ultima_atualizacao_formatada', data)
        # Como o horário acabou de ser criado, deve ser "Agora mesmo"
        self.assertEqual(data['ultima_atualizacao_formatada'], "Agora mesmo")