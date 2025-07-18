from rest_framework import serializers
from django.utils import timezone
from .models import CustomUser, Disciplina, Horario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'tipo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
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
    class Meta:
        model = Horario
        fields = '__all__'

    def validate(self, data):
        instance = self.instance
        professor_monitor = data.get('professor_monitor', getattr(instance, 'professor_monitor', None))
        dia_semana = data.get('dia_semana', getattr(instance, 'dia_semana', None))
        hora_inicio = data.get('hora_inicio', getattr(instance, 'hora_inicio', None))
        hora_fim = data.get('hora_fim', getattr(instance, 'hora_fim', None))

        if hora_inicio and hora_fim and hora_inicio >= hora_fim:
            raise serializers.ValidationError("A hora de início deve ser anterior à hora de fim.")

        if professor_monitor and dia_semana and hora_inicio and hora_fim:
            qs = Horario.objects.filter(
                professor_monitor=professor_monitor,
                dia_semana=dia_semana,
                hora_inicio__lt=hora_fim,
                hora_fim__gt=hora_inicio
            )
            if instance:
                qs = qs.exclude(pk=instance.pk)
            
            if qs.exists():
                raise serializers.ValidationError("Conflito de horário. O professor/monitor já possui um horário neste intervalo.")
        
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
        """Retorna o tempo desde a última atualização em formato legível"""
        agora = timezone.now()
        diferenca = agora - obj.ultima_atualizacao
        
        # Converter para dias, horas, minutos
        dias = diferenca.days
        horas = diferenca.seconds // 3600
        minutos = (diferenca.seconds % 3600) // 60
        
        if dias > 0:
            return f"{dias} dia(s) atrás"
        elif horas > 0:
            return f"{horas} hora(s) atrás"
        elif minutos > 0:
            return f"{minutos} minuto(s) atrás"
        else:
            return "Agora mesmo"


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
        """Retorna a data de última atualização em formato legível"""
        agora = timezone.now()
        diferenca = agora - obj.ultima_atualizacao
        
        # Converter para dias, horas, minutos
        dias = diferenca.days
        horas = diferenca.seconds // 3600
        minutos = (diferenca.seconds % 3600) // 60
        
        if dias > 0:
            return f"{dias} dia(s) atrás"
        elif horas > 0:
            return f"{horas} hora(s) atrás"
        elif minutos > 0:
            return f"{minutos} minuto(s) atrás"
        else:
            return "Agora mesmo"


