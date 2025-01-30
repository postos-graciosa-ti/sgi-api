# RH-API

Bem-vindo ao repositório do RH-API! Este projeto é uma API para gerenciar recursos humanos, incluindo candidatos, funcionários, escalas, departamentos, e muito mais.

## Índice

- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Visão Geral

O RH-API é uma API desenvolvida para gerenciar diversos aspectos de recursos humanos, como candidatos, funcionários, escalas de trabalho, departamentos, entre outros. A API é construída utilizando FastAPI e SQLModel para fornecer uma interface rápida e eficiente para operações CRUD.

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para construir APIs com Python.
- **SQLModel**: Biblioteca para interagir com bancos de dados SQL usando Python.
- **SQLite**: Banco de dados SQL leve e autônomo.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Pydantic**: Validação de dados usando modelos de Python.
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI.

## Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento:

1. **Clone o repositório**:

```bash
git clone https://github.com/seu-usuario/rh-api.git
cd rh-api
```

2. **Crie um ambiente virtual e ative-o**:

```bash python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate` 
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis:

```bash
SQLITE_URL=sqlite:///./database.db
SECRET=your_secret_key
ALGORITHM=HS256
FRONT_URL=http://localhost:3000
```

5. Inicie o servidor de desenvolvimento:

```bash
uvicorn main:app --reload
```

A API estará disponível em http://localhost:8000.

## Uso

Após iniciar o servidor de desenvolvimento, você pode acessar a documentação interativa da API via navegador em http://localhost:8000/docs ou http://localhost:8000/redoc.

## Estrutura do projeto

rh-api/
├── controllers/
│   ├── candidates.py
│   ├── candidato.py
│   ├── cities_states.py
│   ├── cities.py
│   ├── cost_center.py
│   ├── departments.py
│   ├── functions.py
│   ├── jobs.py
│   ├── months.py
│   ├── roles.py
│   ├── root.py
│   ├── scale.py
│   ├── scales_controller.py
│   ├── scales_logs.py
│   ├── scales_reports.py
│   ├── states.py
│   ├── subsidiaries_notifications.py
│   ├── subsidiaries.py
│   ├── turn.py
│   ├── users.py
│   └── workers.py
├── database/
│   └── sqlite.py
├── functions/
│   ├── auth.py
│   ├── excel.py
│   └── handle_operation.py
├── middlewares/
│   └── cors_middleware.py
├── models/
│   ├── candidate.py
│   ├── candidate_status.py
│   ├── candidate_step.py
│   ├── cities.py
│   ├── cost_center.py
│   ├── default_scale.py
│   ├── department.py
│   ├── function.py
│   ├── jobs.py
│   ├── month.py
│   ├── role.py
│   ├── scale.py
│   ├── scale_logs.py
│   ├── scale_signature.py
│   ├── states.py
│   ├── subsidiarie.py
│   ├── subsidiaries_functions_limits.py
│   ├── turn.py
│   ├── user.py
│   ├── user_subsidiaries.py
│   └── workers.py
├── pyhints/
│   ├── cities.py
│   ├── scales.py
│   ├── states.py
│   ├── subsidiaries.py
│   ├── turns.py
│   └── users.py
├── repository/
│   ├── functions.py
│   ├── raw_queries.py
│   └── scale.py
├── scripts/
│   ├── cities_states.py
│   └── excel_scraping.py
├── seeds/
│   └── seed_all.py
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── vercel.json

## Padrões de Nomeação

### Branches
- Use o prefixo feature/ para novas funcionalidades (ex: feature/nova-funcionalidade)
- Use o prefixo bugfix/ para correções de bugs (ex: bugfix/corrige-bug)
- Use o prefixo hotfix/ para correções urgentes (ex: hotfix/corrige-erro-crítico)

### Commits
- Use o tempo presente (ex: feature: Adiciona nova funcionalidade)
- Seja claro e descritivo
- Exemplos:
```feature: Adiciona endpoint para criar usuário```
```bugfix: Corrige erro na autenticação```
```chore: Atualiza dependências```