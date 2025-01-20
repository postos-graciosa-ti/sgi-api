from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from database.sqlite import engine
from models.user import User


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
