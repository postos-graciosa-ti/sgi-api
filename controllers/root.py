import logging

from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy_utils import database_exists
from sqlmodel import Session, SQLModel, select

from database.sqlite import create_db_and_tables, engine
from models import *
from models.user import User
from seeds.seed_all import seed_database

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def update_tables():
    inspector = inspect(engine)

    with engine.connect() as connection:
        for table_name, model in SQLModel.metadata.tables.items():
            if table_name in inspector.get_table_names():
                existing_columns = {
                    col["name"] for col in inspector.get_columns(table_name)
                }

                model_columns = set(model.columns.keys())

                new_columns = model_columns - existing_columns

                if new_columns:
                    for column in new_columns:
                        column_obj = model.columns[column]

                        alter_stmt = f'ALTER TABLE "{table_name}" ADD COLUMN "{column}" {column_obj.type}'

                        connection.execute(alter_stmt)
            else:
                model.create(engine)


def handle_on_startup():
    try:
        update_tables()

    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


def handle_get_docs_info():
    try:
        return {"docs": "acess /docs", "redocs": "access /redocs"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


def handle_health_check():
    try:
        logger.info("Iniciando o health check...")

        with Session(engine) as session:
            inspector = inspect(engine)

            tables = inspector.get_table_names()

            if "user" not in tables:
                logger.warning("Tabela 'user' não encontrada no banco de dados.")

                return {
                    "success": False,
                    "detail": "Tabela 'user' não encontrada no banco de dados.",
                }

            logger.info("Tabela 'user' encontrada. Verificando usuários...")

            has_users = session.scalar(select(User)) is not None

            logger.info(f"Usuário encontrado: {has_users}")

            return {"success": True, "activated": has_users}

    except SQLAlchemyError as e:
        logger.error(f"Erro no banco de dados: {e}")

        return {"success": False, "detail": "Operação no banco de dados falhou."}

    except Exception as e:
        logger.exception("Ocorreu um erro inesperado")

        return {"success": False, "detail": "Ocorreu um erro inesperado."}
