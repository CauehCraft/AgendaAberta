from rest_framework.exceptions import APIException
from rest_framework import status


class AgendaAbertaErrors:
    """
    Dicionário de códigos de erro padronizados para o sistema Agenda Aberta.
    Cada erro contém um código, uma mensagem e um status HTTP.
    """
    HORARIO_CONFLITO = {
        'code': 'HORARIO_CONFLITO',
        'message': 'Conflito de horário detectado',
        'status': status.HTTP_400_BAD_REQUEST
    }
    
    HORARIO_PASSADO = {
        'code': 'HORARIO_PASSADO',
        'message': 'Não é possível editar horários passados',
        'status': status.HTTP_400_BAD_REQUEST
    }
    
    CAMPOS_OBRIGATORIOS = {
        'code': 'CAMPOS_OBRIGATORIOS',
        'message': 'Campos obrigatórios não preenchidos',
        'status': status.HTTP_400_BAD_REQUEST
    }
    
    PERMISSAO_NEGADA = {
        'code': 'PERMISSAO_NEGADA',
        'message': 'Você não tem permissão para realizar esta operação',
        'status': status.HTTP_403_FORBIDDEN
    }
    
    RECURSO_NAO_ENCONTRADO = {
        'code': 'RECURSO_NAO_ENCONTRADO',
        'message': 'O recurso solicitado não foi encontrado',
        'status': status.HTTP_404_NOT_FOUND
    }
    
    ERRO_INTERNO = {
        'code': 'ERRO_INTERNO',
        'message': 'Ocorreu um erro interno no servidor',
        'status': status.HTTP_500_INTERNAL_SERVER_ERROR
    }


class BusinessRuleException(APIException):
    """
    Exceção customizada para regras de negócio.
    Permite definir um código de erro, uma mensagem e um status HTTP.
    """
    def __init__(self, error_dict, detail=None):
        self.error_dict = error_dict
        self.status_code = error_dict['status']
        
        if detail:
            self.detail = {
                'code': error_dict['code'],
                'message': detail
            }
        else:
            self.detail = {
                'code': error_dict['code'],
                'message': error_dict['message']
            }
        
        super().__init__(self.detail)


def custom_exception_handler(exc, context):
    """
    Handler de exceções customizado para o DRF.
    Formata as exceções de forma padronizada.
    """
    from rest_framework.views import exception_handler
    
    # Chamar o handler padrão primeiro
    response = exception_handler(exc, context)
    
    # Se for uma BusinessRuleException, já está formatada corretamente
    if isinstance(exc, BusinessRuleException):
        return response
    
    # Se for outra exceção tratada pelo DRF
    if response is not None:
        # Formatar a resposta de erro
        if isinstance(response.data, dict):
            # Se for um dicionário com detalhes de erro
            if 'detail' in response.data:
                response.data = {
                    'code': f'ERROR_{response.status_code}',
                    'message': response.data['detail']
                }
            else:
                # Se for um dicionário com erros de validação
                errors = {}
                for field, error_list in response.data.items():
                    if isinstance(error_list, list):
                        errors[field] = error_list[0]
                    else:
                        errors[field] = str(error_list)
                
                response.data = {
                    'code': f'VALIDATION_ERROR',
                    'message': 'Erro de validação',
                    'errors': errors
                }
        elif isinstance(response.data, list):
            # Se for uma lista de erros
            response.data = {
                'code': f'ERROR_{response.status_code}',
                'message': response.data[0] if response.data else 'Erro desconhecido'
            }
    
    return response