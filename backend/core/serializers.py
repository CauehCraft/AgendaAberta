from rest_framework import serializers
from .models import Agendamento, CustomUser, Disciplina, Horario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'tipo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

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

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'
