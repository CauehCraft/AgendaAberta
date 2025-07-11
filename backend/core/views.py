from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Agendamento, CustomUser, Horario
from .permissions import IsOwner, IsProfessorOrMonitor
from .serializers import AgendamentoSerializer, HorarioSerializer, UserSerializer

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

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Horario.objects.none()
        if self.request.user.tipo in ['professor', 'monitor']:
            return Horario.objects.filter(professor_monitor=self.request.user)
        return Horario.objects.all()

class AgendamentoViewSet(viewsets.ModelViewSet):
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
