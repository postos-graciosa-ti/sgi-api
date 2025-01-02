# Overview

API do SGI (Sistema de Gestão Integrado) da rede de postos Graciosa

### Tech stack:

- FastApi, um framework web para construir APIs

- SQLModel, uma biblioteca para interagir com bancos de dados SQL a partir de código Python

- Uvicorn, um servidor web ASGI para Python

### Padrões nos nomes de branches:

#### Composição:

- <categoria>/<o que a branch faz em si>

#### Categorias

- docs/ apenas mudanças de documentação;

- feature/ O nome já diz também o que é, uma nova feature que será adicionada ao projeto, componente e afins;

- fix/ a correção de um bug;

- perf/ mudança de código focada em melhorar performance;

- refactor/ mudança de código que não adiciona uma funcionalidade e também não corrigi um bug;

- style/ mudanças no código que não afetam seu significado (espaço em branco, formatação, ponto e vírgula, etc);

- test/ adicionar ou corrigir testes.

- improvement/ Uma melhoria em algo já existente, seja de performance, de escrita, de layout, etc.

#### exemplos:

- refactor/create-password

- feature/insert-or-update-scales

- fix/scale-calculate

### Padrões nos nomes dos Commits:

#### Composição:

- <categoria>: <o que a branch faz em si>

#### Categorias:

- docs: apenas mudanças de documentação;

- feat: O nome já diz também o que é, uma nova feature que será adicionada ao projeto, componente e afins;

- fix: a correção de um bug;

- perf: mudança de código focada em melhorar performance;

- refactor: mudança de código que não adiciona uma funcionalidade e também não corrigi um bug;

- style: mudanças no código que não afetam seu significado (espaço em branco, formatação, ponto e vírgula, etc);

- test: adicionar ou corrigir testes.

- improvement: Uma melhoria em algo já existente, seja de performance, de escrita, de layout, etc.

#### Exemplos:

- refactor: create password

- feature: insert or update scales

- fix: scale calculate

### Padrão de projeto:



# Iniciando

### Clonando o projeto:

```bash
git clone https://github.com/postos-graciosa-ti/sgi-api.git
```

### Adicionando o arquivo .env:

```bash
SQLITE_URL=your_sqlite_connection_string

FRONT_URL=your_front_url
```

### Criando um ambiente virtual:

```bash
cd sgi-api
```

```bash
py -m venv venv
```

### Ativando o ambiente virtual:

```bash
.\venv\Scripts\activate
```

### Instalando as dependências:

```bash
py -m pip install -r requirements.txt
```

### Rodando o projeto localmente:

```bash
py -m uvicorn main:app --reload
```