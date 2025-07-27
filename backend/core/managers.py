from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Manager customizado para o modelo CustomUser com campo 'tipo' obrigatório.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o username, email e senha fornecidos.
        """
        if not email:
            raise ValueError('O campo Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Cria e salva um Superusuário com o username, email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Adiciona a lógica para o campo 'tipo' do superusuário
        # Por padrão, um superusuário será um 'professor'
        extra_fields.setdefault('tipo', 'professor')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)