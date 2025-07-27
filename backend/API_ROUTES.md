# Documentação das Rotas da API - Agenda Aberta

Este documento descreve as rotas da API do backend do sistema Agenda Aberta.

---

## 1. Autenticação

### 1.1. Registro de Usuário

Permite que novos usuários se registrem no sistema.

-   **URL:** `/api/register/`
-   **Método:** `POST`
-   **Permissões:** `AllowAny` (qualquer um pode registrar)

**Corpo da Requisição (JSON):**

```json
{
    "username": "novo_usuario",
    "password": "senha_segura_123",
    "tipo": "aluno" // ou "professor", "monitor"
}
```

**Resposta de Sucesso (201 Created):**

```json
{
    "id": 1,
    "username": "novo_usuario",
    "tipo": "aluno"
}
```

**Resposta de Erro (400 Bad Request):**

```json
{
    "username": [
        "A user with that username already exists."
    ]
}
```

---

### 1.2. Login (Obter Token de Acesso)

Permite que usuários autenticados obtenham um token de acesso JWT.

-   **URL:** `/api/login/`
-   **Método:** `POST`
-   **Permissões:** `AllowAny`

**Corpo da Requisição (JSON):**

```json
{
    "username": "usuario_existente",
    "password": "senha_do_usuario"
}
```

**Resposta de Sucesso (200 OK):**

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Resposta de Erro (401 Unauthorized):**

```json
{
    "detail": "No active account found with the given credentials"
}
```

---

### 1.3. Refresh Token

Permite renovar o token de acesso JWT usando o token de refresh.

-   **URL:** `/api/login/refresh/`
-   **Método:** `POST`
-   **Permissões:** `AllowAny`

**Corpo da Requisição (JSON):**

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Resposta de Sucesso (200 OK):**

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Resposta de Erro (401 Unauthorized):**

```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

---

### 1.4. Excluir Usuário

Permite que um usuário autenticado exclua sua própria conta.

-   **URL:** `/api/delete-user/`
-   **Método:** `DELETE`
-   **Permissões:** `IsAuthenticated` (requer token de acesso)

**Cabeçalhos da Requisição:**

```
Authorization: Bearer <seu_token_de_acesso>
```

**Resposta de Sucesso (204 No Content):**

(Nenhum corpo de resposta)

**Resposta de Erro (401 Unauthorized):**

```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## 2. Horários (Gerenciamento por Professores/Monitores)

Endpoints para criar, listar, atualizar e excluir horários.

-   **URL Base:** `/api/horarios/`
-   **Permissões:** `IsAuthenticated`, `IsProfessorOrMonitor`, `IsOwner` (apenas o proprietário pode editar/excluir seus próprios horários).

**Cabeçalhos da Requisição (para todas as operações abaixo, exceto `GET` público):**

```
Authorization: Bearer <seu_token_de_acesso>
```

---

### 2.1. Listar Horários (Privado)

Lista todos os horários do professor/monitor autenticado.

-   **URL:** `/api/horarios/`
-   **Método:** `GET`

**Parâmetros de Query (Opcionais para Filtragem):**

-   `dia_semana`: Filtrar por dia da semana (ex: `segunda`).
-   `disciplina__curso`: Filtrar por curso da disciplina (ex: `Ciencia da Computacao`).
-   `disciplina`: Filtrar por ID da disciplina (ex: `1`).
-   `search`: Pesquisar por nome do professor/monitor, nome da disciplina ou local.
-   `ordering`: Ordenar resultados (ex: `hora_inicio`, `-ultima_atualizacao`).

**Resposta de Sucesso (200 OK):**

```json
[
    {
        "id": 1,
        "disciplina": {
            "id": 1,
            "nome": "Programação Web",
            "curso": "Engenharia de Software",
            "codigo": "WEB101",
            "semestre": 5,
            "ativo": true
        },
        "professor_monitor": {
            "id": 2,
            "username": "professor_joao",
            "tipo": "professor",
            "nome_completo": "João Silva"
        },
        "dia_semana": "segunda",
        "hora_inicio": "09:00:00",
        "hora_fim": "10:00:00",
        "local": "Sala B201",
        "ultima_atualizacao": "2024-07-16T10:30:00Z",
        "data_criacao": "2024-07-15T10:00:00Z",
        "ativo": true,
        "tempo_desde_atualizacao": "1 dia(s) atrás"
    }
]
```

---

### 2.2. Criar Horário

Cria um novo horário para o professor/monitor autenticado.

-   **URL:** `/api/horarios/`
-   **Método:** `POST`

**Corpo da Requisição (JSON):**

```json
{
    "disciplina": 1, // ID da disciplina
    "dia_semana": "terca",
    "hora_inicio": "14:00",
    "hora_fim": "15:30",
    "local": "Laboratório de Redes"
    // "professor_monitor" é preenchido automaticamente pelo usuário autenticado
}
```

**Resposta de Sucesso (201 Created):**

```json
{
    "data": {
        "id": 2,
        "disciplina": 1,
        "professor_monitor": 2,
        "dia_semana": "terca",
        "hora_inicio": "14:00:00",
        "hora_fim": "15:30:00",
        "local": "Laboratório de Redes",
        "ultima_atualizacao": "2024-07-16T15:00:00Z",
        "data_criacao": "2024-07-16T15:00:00Z",
        "ativo": true
    },
    "message": "Horário cadastrado com sucesso!",
    "status_code": 201
}
```

**Resposta de Erro (400 Bad Request):**

```json
{
    "message": "Conflito de horário detectado. Você já possui um horário cadastrado que se sobrepõe a este.",
    "code": "HORARIO_CONFLITO"
}
```

---

### 2.3. Detalhes do Horário

Obtém os detalhes de um horário específico.

-   **URL:** `/api/horarios/{id}/`
-   **Método:** `GET`

**Resposta de Sucesso (200 OK):**

```json
{
    "id": 1,
    "disciplina": {
        "id": 1,
        "nome": "Programação Web",
        "curso": "Engenharia de Software",
        "codigo": "WEB101",
        "semestre": 5,
        "ativo": true
    },
    "professor_monitor": {
        "id": 2,
        "username": "professor_joao",
        "tipo": "professor",
        "nome_completo": "João Silva"
    },
    "dia_semana": "segunda",
    "hora_inicio": "09:00:00",
    "hora_fim": "10:00:00",
    "local": "Sala B201",
    "ultima_atualizacao": "2024-07-16T10:30:00Z",
    "data_criacao": "2024-07-15T10:00:00Z",
    "ativo": true,
    "tempo_desde_atualizacao": "1 dia(s) atrás"
}
```

---

### 2.4. Atualizar Horário

Atualiza um horário existente.

-   **URL:** `/api/horarios/{id}/`
-   **Método:** `PUT` (atualização completa) ou `PATCH` (atualização parcial)

**Corpo da Requisição (JSON - exemplo PATCH):**

```json
{
    "local": "Sala B202"
}
```

**Resposta de Sucesso (200 OK):**

```json
{
    "data": {
        "id": 1,
        "disciplina": 1,
        "professor_monitor": 2,
        "dia_semana": "segunda",
        "hora_inicio": "09:00:00",
        "hora_fim": "10:00:00",
        "local": "Sala B202",
        "ultima_atualizacao": "2024-07-16T15:30:00Z",
        "data_criacao": "2024-07-15T10:00:00Z",
        "ativo": true
    },
    "message": "Horário atualizado com sucesso!",
    "status_code": 200
}
```

---

### 2.5. Excluir Horário

Exclui um horário existente.

-   **URL:** `/api/horarios/{id}/`
-   **Método:** `DELETE`

**Resposta de Sucesso (200 OK):**

```json
{
    "message": "Horário excluído com sucesso!",
    "status_code": 200
}
```

---

## 3. Horários Públicos (Visualização para Alunos/Visitantes)

Endpoints para visualizar horários sem necessidade de autenticação.

-   **URL Base:** `/api/horarios-publicos/`
-   **Permissões:** `AllowAny`

---

### 3.1. Listar Horários Públicos

Lista todos os horários ativos disponíveis para visualização.

-   **URL:** `/api/horarios-publicos/`
-   **Método:** `GET`

**Parâmetros de Query (Opcionais para Filtragem):**

-   `dia_semana`: Filtrar por dia da semana (ex: `segunda`).
-   `disciplina`: Filtrar por ID da disciplina (ex: `1`).
-   `curso`: Filtrar por curso da disciplina (ex: `Engenharia de Software`).
-   `professor`: Filtrar por nome de usuário do professor/monitor (ex: `professor_joao`).
-   `search`: Pesquisar por nome da disciplina, código da disciplina, nome de usuário do professor/monitor ou local.
-   `ordering`: Ordenar resultados (ex: `hora_inicio`, `-ultima_atualizacao`).

**Resposta de Sucesso (200 OK):**

```json
{
    "results": [
        {
            "id": 1,
            "dia_semana": "segunda",
            "hora_inicio": "09:00:00",
            "hora_fim": "10:00:00",
            "local": "Sala B201",
            "disciplina_nome": "Programação Web",
            "disciplina_codigo": "WEB101",
            "curso": "Engenharia de Software",
            "professor_nome": "João Silva",
            "ultima_atualizacao_formatada": "1 dia(s) atrás"
        }
    ],
    "message": "Este sistema é apenas para visualização de horários disponíveis, não para agendamento."
}
```

---

### 3.2. Detalhes do Horário Público

Obtém os detalhes de um horário específico para visualização pública.

-   **URL:** `/api/horarios-publicos/{id}/`
-   **Método:** `GET`

**Resposta de Sucesso (200 OK):**

```json
{
    "id": 1,
    "dia_semana": "segunda",
    "hora_inicio": "09:00:00",
    "hora_fim": "10:00:00",
    "local": "Sala B201",
    "disciplina_nome": "Programação Web",
    "disciplina_codigo": "WEB101",
    "curso": "Engenharia de Software",
    "professor_nome": "João Silva",
    "ultima_atualizacao_formatada": "1 dia(s) atrás",
    "message": "Este sistema é apenas para visualização de horários disponíveis, não para agendamento."
}
```

---

## 4. Disciplinas

Endpoints para criar, listar, atualizar e excluir disciplinas.

-   **URL Base:** `/api/disciplinas/`
-   **Permissões:** `IsAuthenticated`

**Cabeçalhos da Requisição (para todas as operações abaixo):**

```
Authorization: Bearer <seu_token_de_acesso>
```

---

### 4.1. Listar Disciplinas

Lista todas as disciplinas cadastradas.

-   **URL:** `/api/disciplinas/`
-   **Método:** `GET`

**Parâmetros de Query (Opcionais para Filtragem):**

-   `search`: Pesquisar por nome, código ou curso da disciplina.
-   `ordering`: Ordenar resultados (ex: `nome`, `codigo`, `semestre`).
-   `ativo`: Filtrar por status ativo (`true` ou `false`).
-   `semestre`: Filtrar por semestre (ex: `3`).
-   `curso`: Filtrar por curso (ex: `Engenharia de Software`).

**Resposta de Sucesso (200 OK):**

```json
[
    {
        "id": 1,
        "nome": "Programação Web",
        "curso": "Engenharia de Software",
        "codigo": "WEB101",
        "semestre": 5,
        "ativo": true
    },
    {
        "id": 2,
        "nome": "Estrutura de Dados",
        "curso": "Ciência da Computação",
        "codigo": "ED202",
        "semestre": 3,
        "ativo": true
    }
]
```

---

### 4.2. Criar Disciplina

Cria uma nova disciplina.

-   **URL:** `/api/disciplinas/`
-   **Método:** `POST`

**Corpo da Requisição (JSON):**

```json
{
    "nome": "Inteligência Artificial",
    "curso": "Ciência da Computação",
    "codigo": "IA303",
    "semestre": 7,
    "ativo": true
}
```

**Resposta de Sucesso (201 Created):**

```json
{
    "data": {
        "id": 3,
        "nome": "Inteligência Artificial",
        "curso": "Ciência da Computação",
        "codigo": "IA303",
        "semestre": 7,
        "ativo": true
    },
    "message": "Disciplina cadastrada com sucesso!",
    "status_code": 201
}
```

---

### 4.3. Detalhes da Disciplina

Obtém os detalhes de uma disciplina específica.

-   **URL:** `/api/disciplinas/{id}/`
-   **Método:** `GET`

**Resposta de Sucesso (200 OK):**

```json
{
    "id": 1,
    "nome": "Programação Web",
    "curso": "Engenharia de Software",
    "codigo": "WEB101",
    "semestre": 5,
    "ativo": true
}
```

---

### 4.4. Atualizar Disciplina

Atualiza uma disciplina existente.

-   **URL:** `/api/disciplinas/{id}/`
-   **Método:** `PUT` (atualização completa) ou `PATCH` (atualização parcial)

**Corpo da Requisição (JSON - exemplo PATCH):**

```json
{
    "ativo": false
}
```

**Resposta de Sucesso (200 OK):**

```json
{
    "data": {
        "id": 1,
        "nome": "Programação Web",
        "curso": "Engenharia de Software",
        "codigo": "WEB101",
        "semestre": 5,
        "ativo": false
    },
    "message": "Disciplina atualizada com sucesso!",
    "status_code": 200
}
```

---

### 4.5. Excluir Disciplina

Exclui uma disciplina existente.

-   **URL:** `/api/disciplinas/{id}/`
-   **Método:** `DELETE`

**Resposta de Sucesso (200 OK):**

```json
{
    "message": "Disciplina excluída com sucesso!",
    "status_code": 200
}
```
