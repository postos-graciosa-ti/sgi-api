# Overview

API do SGI (Sistema de Gestão Integrado) da rede de postos Graciosa

### Tech stack:

- FastApi, um framework web para construir APIs

- SQLModel, uma biblioteca para interagir com bancos de dados SQL a partir de código Python

- Uvicorn, um servidor web ASGI para Python

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