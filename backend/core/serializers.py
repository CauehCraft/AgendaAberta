from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Disciplina, Horario
from .utils import humanize_time_since
from .validators import HorarioValidator

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'tipo', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if ' ' in value:
            raise serializers.ValidationError("O nome de usuário não pode conter espaços.")
        if CustomUser.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def validate_email(self, value):
        email = value.lower()
        if not (email.endswith('@ufersa.edu.br') or email.endswith('@alunos.ufersa.edu.br')):
            raise serializers.ValidationError("O email deve ser de um domínio da UFERSA (@ufersa.edu.br ou @alunos.ufersa.edu.br).")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Este endereço de email já está em uso.")
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            tipo=validated_data['tipo'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class UserBasicSerializer(serializers.ModelSerializer):
    """Serializer básico para usuários, sem informações sensíveis"""
    nome_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'tipo', 'nome_completo')
    
    def get_nome_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    """
    Serializer para criar e atualizar horários.
    Agora centraliza toda a lógica de validação de dados chamando HorarioValidator.
    """
    class Meta:
        model = Horario
        # Lista explícita de campos é uma boa prática
        fields = [
            'id', 
            'disciplina', 
            'dia_semana', 
            'hora_inicio', 
            'hora_fim', 
            'local', 
            'professor_monitor', # Será preenchido automaticamente pela view
            'ativo', 
            'ultima_atualizacao', 
            'data_criacao'
        ]
        # Garante que o usuário não pode atribuir um horário a outra pessoa
        read_only_fields = ['professor_monitor']

    def validate(self, data):
        """
        Método de validação centralizado. É executado em operações de create e update.
        """
        # O DRF passa a instância (em updates) e o contexto (que contém a request)
        instance = self.instance
        user = self.context['request'].user

        # Coleta os dados para validação, usando os novos dados ou os da instância existente
        disciplina = data.get('disciplina', getattr(instance, 'disciplina', None))
        local = data.get('local', getattr(instance, 'local', None))
        dia_semana = data.get('dia_semana', getattr(instance, 'dia_semana', None))
        hora_inicio = data.get('hora_inicio', getattr(instance, 'hora_inicio', None))
        hora_fim = data.get('hora_fim', getattr(instance, 'hora_fim', None))
        
        # --- ETAPA 1: Validar campos obrigatórios ---
        try:
            HorarioValidator.validate_required_fields(disciplina=disciplina, local=local)
        except DjangoValidationError as e:
            # Converte o erro padrão do Django para um erro do DRF para consistência na API
            raise serializers.ValidationError(e.message_dict)

        # --- ETAPA 2: Validar a ordem cronológica das horas ---
        if hora_inicio and hora_fim and hora_inicio >= hora_fim:
            raise serializers.ValidationError({"hora_fim": "A hora de fim deve ser posterior à hora de início."})

        # --- ETAPA 3: Validar conflito de horário para o próprio professor/monitor ---
        exclude_id = instance.id if instance else None
        if not HorarioValidator.validate_schedule_conflict(
            professor=user,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            exclude_id=exclude_id
        ):
            # Este é um erro geral, não específico de um campo
            raise serializers.ValidationError("Conflito de horário. Você já possui um atendimento neste intervalo.")

        # --- ETAPA 4: Validar conflito de uso da sala/local ---
        if local and dia_semana and hora_inicio and hora_fim:
            conflito_de_sala = Horario.objects.filter(
                local=local,
                dia_semana=dia_semana,
                hora_inicio__lt=hora_fim,
                hora_fim__gt=hora_inicio
            )
            if instance:
                conflito_de_sala = conflito_de_sala.exclude(pk=instance.pk)
            
            if conflito_de_sala.exists():
                raise serializers.ValidationError(
                    {"local": "Conflito de agendamento: Esta sala já está reservada neste mesmo horário."}
                )
        
        # Se todas as validações passaram, retorna os dados
        return data


class HorarioDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado para horários, incluindo dados relacionados"""
    disciplina = DisciplinaSerializer(read_only=True)
    professor_monitor = UserBasicSerializer(read_only=True)
    tempo_desde_atualizacao = serializers.SerializerMethodField()
    
    class Meta:
        model = Horario
        fields = '__all__'
    
    def get_tempo_desde_atualizacao(self, obj):
        return humanize_time_since(obj.ultima_atualizacao)


class HorarioPublicSerializer(serializers.ModelSerializer):
    """Serializer para visualização pública de horários, sem informações sensíveis"""
    disciplina_nome = serializers.CharField(source='disciplina.nome', read_only=True)
    disciplina_codigo = serializers.CharField(source='disciplina.codigo', read_only=True)
    curso = serializers.CharField(source='disciplina.curso', read_only=True)
    professor_nome = serializers.SerializerMethodField()
    ultima_atualizacao_formatada = serializers.SerializerMethodField()
    
    class Meta:
        model = Horario
        fields = [
            'id', 'dia_semana', 'hora_inicio', 'hora_fim', 'local',
            'disciplina_nome', 'disciplina_codigo', 'curso',
            'professor_nome', 'ultima_atualizacao_formatada'
        ]
    
    def get_professor_nome(self, obj):
        """Retorna o nome do professor/monitor"""
        if obj.professor_monitor.first_name or obj.professor_monitor.last_name:
            return f"{obj.professor_monitor.first_name} {obj.professor_monitor.last_name}".strip()
        return obj.professor_monitor.username
    
    def get_ultima_atualizacao_formatada(self, obj):
        return humanize_time_since(obj.ultima_atualizacao)


