from rest_framework import generics, viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError

from .models import CustomUser, Disciplina, Horario
from .permissions import IsOwner, IsProfessorOrMonitor
from .serializers import (
    DisciplinaSerializer, HorarioSerializer, UserSerializer,
    HorarioDetailSerializer, HorarioPublicSerializer, UserBasicSerializer
)
from .validators import HorarioValidator
from .filters import HorarioFilter
from .responses import ApiResponse

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response(status=204)

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all().select_related('disciplina', 'professor_monitor')
    permission_classes = [IsAuthenticated, IsProfessorOrMonitor, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dia_semana', 'disciplina__curso', 'disciplina']
    search_fields = ['professor_monitor__username', 'disciplina__nome', 'local']
    ordering_fields = ['dia_semana', 'hora_inicio', 'hora_fim', 'ultima_atualizacao']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado com base na ação."""
        if self.action in ['list', 'retrieve']:
            return HorarioDetailSerializer
        return HorarioSerializer
        
    def get_queryset(self):
        """Filtra os horários para mostrar apenas os do usuário logado."""
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Horario.objects.none()
        # Assume que 'professor' e 'monitor' são os tipos que podem criar horários
        if self.request.user.tipo in ['professor', 'monitor']:
            return Horario.objects.filter(professor_monitor=self.request.user)
        # Admins podem ver tudo (ajuste conforme sua regra de negócio)
        return Horario.objects.all()

    def perform_create(self, serializer):
        serializer.save(professor_monitor=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        if not HorarioValidator.validate_future_schedule(horario_instance=instance):
            raise ValidationError("Não é possível excluir um horário que já ocorreu.")
        
        instance.delete()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return ApiResponse.success(
            data=serializer.data,
            message="Horário cadastrado com sucesso!",
            status_code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            
        return ApiResponse.success(
            data=serializer.data,
            message="Horário atualizado com sucesso!",
            status_code=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance) # A validação ocorre dentro deste método
        return ApiResponse.success(
            message="Horário excluído com sucesso!",
            status_code=status.HTTP_200_OK
        )

@method_decorator(cache_page(60 * 15), name='dispatch')
class HorarioPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualização pública de horários, com cache e filtros otimizados.
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

    
class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'codigo', 'curso']
    ordering_fields = ['nome', 'codigo', 'curso', 'semestre']
    
    def create(self, request, *args, **kwargs):
        """Sobrescreve o método create para fornecer feedback claro"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return ApiResponse.success(
            data=serializer.data,
            message="Disciplina cadastrada com sucesso!",
            status_code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Sobrescreve o método update para fornecer feedback claro"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            
        return ApiResponse.success(
            data=serializer.data,
            message="Disciplina atualizada com sucesso!",
            status_code=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        """Sobrescreve o método destroy para fornecer feedback claro"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(
            message="Disciplina excluída com sucesso!",
            status_code=status.HTTP_200_OK
        )
    
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

class MeView(APIView):
    """
    Retorna os dados do usuário atualmente autenticado.
    """
    permission_classes = [IsAuthenticated] # Garante que apenas usuários logados podem acessar
    serializer_class = UserBasicSerializer # Define o serializer que será usado

    def get(self, request, *args, **kwargs):
        """
        Pega o usuário da requisição e o serializa com UserBasicSerializer.
        """
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)