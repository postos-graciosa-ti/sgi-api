import logging

from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from database.sqlite import create_db_and_tables, engine
from models.user import User
from seeds.seed_all import seed_database

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


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