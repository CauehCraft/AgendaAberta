from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    DeleteUserView, DisciplinaViewSet, 
    HorarioViewSet, HorarioPublicViewSet, RegisterView
)

router = DefaultRouter()
router.register(r'disciplinas', DisciplinaViewSet)
router.register(r'horarios', HorarioViewSet)
router.register(r'horarios-publicos', HorarioPublicViewSet, basename='horario-publico')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete-user/', DeleteUserView.as_view(), name='delete_user'),
    path('', include(router.urls)),
]