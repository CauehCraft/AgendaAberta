from rest_framework import generics, viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Agendamento, CustomUser, Disciplina, Horario
from .permissions import IsOwner, IsProfessorOrMonitor
from .serializers import (
    AgendamentoSerializer, DisciplinaSerializer, HorarioSerializer, UserSerializer,
    HorarioDetailSerializer, HorarioPublicSerializer, UserBasicSerializer
)
from .validators import HorarioValidator
from .exceptions import BusinessRuleException, AgendaAbertaErrors
from .filters import HorarioFilter

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response(status=204)

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [IsAuthenticated, IsProfessorOrMonitor, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dia_semana', 'disciplina__curso', 'disciplina']
    search_fields = ['professor_monitor__username', 'disciplina__nome', 'local']
    ordering_fields = ['dia_semana', 'hora_inicio', 'hora_fim', 'ultima_atualizacao']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado com base na ação"""
        if self.action in ['list', 'retrieve']:
            return HorarioDetailSerializer
        return HorarioSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Horario.objects.none()
        if self.request.user.tipo in ['professor', 'monitor']:
            return Horario.objects.filter(professor_monitor=self.request.user)
        return Horario.objects.all()
    
    def perform_create(self, serializer):
        """Validar campos obrigatórios e conflitos antes de criar"""
        try:
            # Validar campos obrigatórios
            disciplina = serializer.validated_data.get('disciplina')
            local = serializer.validated_data.get('local')
            HorarioValidator.validate_required_fields(disciplina=disciplina, local=local)
            
            # Validar conflitos de horário
            dia_semana = serializer.validated_data.get('dia_semana')
            hora_inicio = serializer.validated_data.get('hora_inicio')
            hora_fim = serializer.validated_data.get('hora_fim')
            
            if not HorarioValidator.validate_schedule_conflict(
                professor=self.request.user,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim
            ):
                raise BusinessRuleException(
                    AgendaAbertaErrors.HORARIO_CONFLITO,
                    'Conflito de horário detectado. Você já possui um horário cadastrado que se sobrepõe a este.'
                )
            
            # Salvar com o professor/monitor atual
            serializer.save(professor_monitor=self.request.user)
            
        except Exception as e:
            if not isinstance(e, BusinessRuleException):
                raise BusinessRuleException(
                    AgendaAbertaErrors.ERRO_INTERNO,
                    str(e)
                )
            raise
    
    def perform_update(self, serializer):
        """Validar se é horário futuro e se não há conflitos antes de atualizar"""
        try:
            instance = self.get_object()
            
            # Validar se é horário futuro
            if not HorarioValidator.validate_future_schedule(horario_instance=instance):
                raise BusinessRuleException(
                    AgendaAbertaErrors.HORARIO_PASSADO,
                    'Não é possível editar horários passados.'
                )
            
            # Validar campos obrigatórios
            disciplina = serializer.validated_data.get('disciplina', instance.disciplina)
            local = serializer.validated_data.get('local', instance.local)
            HorarioValidator.validate_required_fields(disciplina=disciplina, local=local)
            
            # Validar conflitos de horário
            dia_semana = serializer.validated_data.get('dia_semana', instance.dia_semana)
            hora_inicio = serializer.validated_data.get('hora_inicio', instance.hora_inicio)
            hora_fim = serializer.validated_data.get('hora_fim', instance.hora_fim)
            
            if not HorarioValidator.validate_schedule_conflict(
                professor=self.request.user,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                exclude_id=instance.id
            ):
                raise BusinessRuleException(
                    AgendaAbertaErrors.HORARIO_CONFLITO,
                    'Conflito de horário detectado. Você já possui um horário cadastrado que se sobrepõe a este.'
                )
            
            serializer.save()
            
        except Exception as e:
            if not isinstance(e, BusinessRuleException):
                raise BusinessRuleException(
                    AgendaAbertaErrors.ERRO_INTERNO,
                    str(e)
                )
            raise
    
    def perform_destroy(self, instance):
        """Validar se é horário futuro antes de excluir"""
        try:
            if not HorarioValidator.validate_future_schedule(horario_instance=instance):
                raise BusinessRuleException(
                    AgendaAbertaErrors.HORARIO_PASSADO,
                    'Não é possível excluir horários passados.'
                )
            instance.delete()
        except Exception as e:
            if not isinstance(e, BusinessRuleException):
                raise BusinessRuleException(
                    AgendaAbertaErrors.ERRO_INTERNO,
                    str(e)
                )
            raise

class HorarioPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualização pública de horários, sem necessidade de autenticação.
    Permite apenas operações de leitura (list, retrieve).
    """
    queryset = Horario.objects.filter(ativo=True).select_related('disciplina', 'professor_monitor')
    serializer_class = HorarioPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HorarioFilter
    search_fields = ['disciplina__nome', 'disciplina__codigo', 'professor_monitor__username', 'local']
    ordering_fields = ['dia_semana', 'hora_inicio', 'hora_fim', 'ultima_atualizacao']
    
    def list(self, request, *args, **kwargs):
        """Adiciona mensagem informativa sobre o propósito do sistema"""
        response = super().list(request, *args, **kwargs)
        if isinstance(response.data, dict):
            response.data['message'] = "Este sistema é apenas para visualização de horários disponíveis, não para agendamento."
        else:
            # Se a resposta não for um dicionário, transforme-a em um
            results = response.data
            response.data = {
                'results': results,
                'message': "Este sistema é apenas para visualização de horários disponíveis, não para agendamento."
            }
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """Adiciona mensagem informativa sobre o propósito do sistema"""
        response = super().retrieve(request, *args, **kwargs)
        if isinstance(response.data, dict):
            response.data['message'] = "Este sistema é apenas para visualização de horários disponíveis, não para agendamento."
        return response
    
    def get_queryset(self):
        """Aplica filtros customizados ao queryset"""
        queryset = super().get_queryset()
        
        # Filtrar por curso
        curso = self.request.query_params.get('curso')
        if curso:
            queryset = queryset.filter(disciplina__curso__icontains=curso)
        
        # Filtrar por disciplina
        disciplina_id = self.request.query_params.get('disciplina')
        if disciplina_id:
            try:
                queryset = queryset.filter(disciplina_id=int(disciplina_id))
            except (ValueError, TypeError):
                pass
        
        # Filtrar por professor/monitor
        professor = self.request.query_params.get('professor')
        if professor:
            queryset = queryset.filter(professor_monitor__username__icontains=professor)
        
        # Filtrar por dia da semana
        dia_semana = self.request.query_params.get('dia_semana')
        if dia_semana:
            queryset = queryset.filter(dia_semana=dia_semana)
        
        return queryset


class AgendamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Agendamento.
    
    Nota: Este sistema é principalmente para visualização de horários disponíveis,
    não para agendamento. O modelo Agendamento existe para registrar interesse em
    horários específicos, mas não é o foco principal do sistema.
    """
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Agendamento.objects.none()
        if self.request.user.tipo == 'aluno':
            return Agendamento.objects.filter(aluno=self.request.user)
        elif self.request.user.tipo in ['professor', 'monitor']:
            return Agendamento.objects.filter(horario__professor_monitor=self.request.user)
        return Agendamento.objects.none()
    
    def list(self, request, *args, **kwargs):
        """Adiciona mensagem informativa sobre o propósito do sistema"""
        response = super().list(request, *args, **kwargs)
        if isinstance(response.data, dict):
            response.data['message'] = "Este sistema é principalmente para visualização de horários disponíveis, não para agendamento."
        else:
            # Se a resposta não for um dicionário, transforme-a em um
            results = response.data
            response.data = {
                'results': results,
                'message': "Este sistema é principalmente para visualização de horários disponíveis, não para agendamento."
            }
        return response
    
    def perform_create(self, serializer):
        """Salva o agendamento com o aluno atual"""
        serializer.save(aluno=self.request.user)

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'codigo', 'curso']
    ordering_fields = ['nome', 'codigo', 'curso', 'semestre']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Disciplina.objects.none()
            
        queryset = Disciplina.objects.all()
        
        # Filter by active status
        ativo = self.request.query_params.get('ativo')
        if ativo is not None:
            ativo_bool = ativo.lower() == 'true'
            queryset = queryset.filter(ativo=ativo_bool)
            
        # Filter by semester
        semestre = self.request.query_params.get('semestre')
        if semestre is not None:
            try:
                semestre_int = int(semestre)
                queryset = queryset.filter(semestre=semestre_int)
            except ValueError:
                pass
                
        # Filter by course
        curso = self.request.query_params.get('curso')
        if curso is not None:
            queryset = queryset.filter(curso__icontains=curso)
            
        return queryset
