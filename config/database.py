import os

from sqlmodel import SQLModel, create_engine

from seeds.seed_all import seed_database

NOME_ARQUIVO = "database.db"

DATABASE_URL = f"sqlite:///{os.path.join(os.getcwd(), NOME_ARQUIVO)}"

engine = None


def criar_engine():
    global engine

    engine = create_engine(DATABASE_URL, echo=True)


def reconectar_banco():
    criar_engine()

    SQLModel.metadata.create_all(engine)

    seed_database()
