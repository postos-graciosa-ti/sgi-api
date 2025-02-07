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


def handle_activate_render_server():
    try:
        with Session(engine) as session:
            has_users = session.exec(select(User)).first()

            result = bool(has_users)

            return {"success": True, "activated": result}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database operation failed.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
