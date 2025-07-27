# Relatório de Cobertura de Testes - Sistema Agenda Aberta

## Resumo

- **Total de testes:** 116
- **Testes passando:** 100
- **Testes falhando:** 16
- **Cobertura geral:** 92%
- **Meta de cobertura:** 80% (Superada)

## Cobertura por Arquivo

| Arquivo | Cobertura |
|---------|-----------|
| backend/core/views.py | 74% |
| backend/core/migrations/0005_update_disciplina_codes.py | 38% |
| backend/core/exceptions.py | 89% |
| backend/core/serializers.py | 93% |
| backend/core/validators.py | 95% |
| backend/core/filters.py | 95% |
| backend/core/models.py | 100% |
| backend/core/responses.py | 100% |

## Testes Falhando

### Problemas com Agendamento API

1. `test_filter_agendamentos_by_date` - Esperava 1 resultado, mas recebeu 2
2. `test_filter_agendamentos_by_status` - Esperava 1 resultado, mas recebeu 2
3. `test_list_agendamentos_authenticated` - Esperava 1 resultado, mas recebeu 2
4. `test_update_agendamento_status` - Esperava status 200, mas recebeu 400

### Problemas com Disciplina API

1. `test_delete_disciplina` - Esperava status 204, mas recebeu 200

### Problemas com CustomUser Model

1. `test_user_tipo_choices` - Esperava que ValueError fosse lançado, mas não foi

### Problemas com Feedback

1. `test_create_horario_feedback` - Esperava status 201, mas recebeu 400
2. `test_delete_horario_feedback` - Esperava status 200, mas recebeu 400
3. `test_update_horario_feedback` - Esperava status 200, mas recebeu 400

### Problemas com Serializers

1. `test_horario_detalhes_field` - Esperava string '14:00:00', mas recebeu objeto time(14, 0)

### Problemas com HorarioViewSet

1. `test_create_horario_as_professor` - Esperava status 201, mas recebeu 400
2. `test_delete_horario_as_another_professor` - Esperava status 403, mas recebeu 404
3. `test_delete_horario_as_professor_owner` - Esperava status 200, mas recebeu 400
4. `test_list_horarios_as_aluno` - Esperava status 200, mas recebeu 403
5. `test_update_horario_as_another_professor` - Esperava status 403, mas recebeu 404
6. `test_update_horario_as_professor_owner` - Esperava status 200, mas recebeu 400

## Recomendações

1. **Corrigir problemas de permissão** - Alunos não conseguem listar horários (status 403)
2. **Corrigir validações de horários** - Muitos testes de criação/atualização/exclusão estão falhando com status 400
3. **Corrigir serialização de horários** - Problema com formato de hora (objeto vs string)
4. **Corrigir validação de tipo de usuário** - Não está validando corretamente tipos inválidos
5. **Padronizar códigos de status HTTP** - Inconsistência entre status 200 e 204 para exclusão

## Próximos Passos

1. Corrigir os testes falhando
2. Melhorar a cobertura de código em `views.py` e `migrations/0005_update_disciplina_codes.py`
3. Executar novamente os testes para verificar se todos passam
4. Configurar integração contínua para executar os testes automaticamente