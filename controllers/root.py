import logging
import os

from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError
from database.sqlite import create_db_and_tables, engine
from models.user import User
from seeds.seed_all import seed_database

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def safe_apply_migrations():
    try:
        alembic_cfg = Config("alembic.ini")

        # Configura logging para evitar saída excessiva (opcional)
        logging.getLogger("alembic").setLevel(logging.WARNING)

        # Verifica e aplica migrações
        command.upgrade(alembic_cfg, "head")
        print("Migrações verificadas e aplicadas com sucesso.")
        return True
    except CommandError as e:
        print(f"Erro ao aplicar migrações: {str(e)}")
        print("Continuando sem aplicar migrações...")
        return False
    except Exception as e:
        print(f"Erro inesperado no Alembic: {str(e)}")
        print("Continuando a execução...")
        return False


def handle_on_startup():
    try:
        database_url = os.environ.get("SQLITE_URL")

        if not database_exists(engine.url):
            print("Banco de dados não encontrado. Criando...")
            create_db_and_tables()
            seed_database()
        else:
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            if not tables:
                print("Nenhuma tabela encontrada. Criando estrutura inicial...")
                create_db_and_tables()
                seed_database()
            else:
                print("Banco de dados existente detectado. Verificando migrações...")

                # Tenta aplicar migrações, mas continua mesmo se falhar
                migration_success = safe_apply_migrations()

                if not migration_success:
                    print(
                        "Atenção: Não foi possível verificar/atualizar completamente as migrações."
                    )
                    print(
                        "O aplicativo continuará, mas o banco de dados pode não estar atualizado."
                    )

                print("Verificação de banco de dados concluída.")

    except OperationalError as e:
        print(f"Erro crítico ao conectar ao banco de dados: {e}")
        # Aqui você pode decidir se quer encerrar o aplicativo ou não
        raise


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
