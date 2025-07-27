from rest_framework.response import Response
from rest_framework import status


class ApiResponse:
    """
    Classe para padronizar as respostas da API.
    Fornece métodos para criar respostas de sucesso e erro com mensagens claras.
    """
    
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        """
        Cria uma resposta de sucesso padronizada.
        
        Args:
            data: Dados a serem retornados
            message: Mensagem de sucesso
            status_code: Código de status HTTP
            
        Returns:
            Response: Resposta padronizada
        """
        response_data = {
            'status': 'success',
        }
        
        if message:
            response_data['message'] = message
        
        if data is not None:
            response_data['data'] = data
            
        # Adicionar mensagem informativa sobre o propósito do sistema
        response_data['system_info'] = "Este sistema é para visualização de horários disponíveis, não para agendamento."
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Cria uma resposta de erro padronizada.
        
        Args:
            message: Mensagem de erro
            errors: Detalhes dos erros
            status_code: Código de status HTTP
            
        Returns:
            Response: Resposta padronizada
        """
        response_data = {
            'status': 'error',
            'message': message
        }
        
        if errors:
            response_data['errors'] = errors
            
        # Adicionar mensagem informativa sobre o propósito do sistema
        response_data['system_info'] = "Este sistema é para visualização de horários disponíveis, não para agendamento."
        
        return Response(response_data, status=status_code)