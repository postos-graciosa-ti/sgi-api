from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from database.sqlite import create_db_and_tables, engine
from models.user import User
from seeds.seed_all import seed_database


def handle_on_startup():
    try:
        if not database_exists(engine.url):
            create_db_and_tables()

            seed_database()

        else:
            inspector = inspect(engine)

            tables = inspector.get_table_names()

            if not tables:
                create_db_and_tables()

                seed_database()

    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


def handle_get_docs_info():
    try:
        return {"docs": "acess /docs", "redocs": "access /redocs"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


def handle_health_check():
    try:
        print("Iniciando o health check...")

        with Session(engine) as session:
            print("Conectando-se ao banco de dados...")

            inspector = inspect(engine)

            print("Inspecionando o banco de dados para tabelas...")

            tables = inspector.get_table_names()

            print(f"Tabelas encontradas: {tables}")

            # Verifica se a tabela 'user' existe
            if "user" not in tables:
                print("Tabela 'user' não encontrada no banco de dados.")

                return {
                    "success": False,
                    "detail": "Tabela 'user' não encontrada no banco de dados.",
                }

            print("Tabela 'user' encontrada.")

            has_users = session.exec(select(User)).first()

            if has_users:
                print(f"Usuário encontrado: {has_users}")

            else:
                print("Nenhum usuário encontrado.")

            result = bool(has_users)

            print(f"Resultado de ativação: {result}")

            return {"success": True, "activated": result}

    except SQLAlchemyError as e:
        print(f"Erro no banco de dados: {e}")

        return {"success": False, "detail": "Operação no banco de dados falhou."}

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

        return {"success": False, "detail": "Ocorreu um erro inesperado."}
