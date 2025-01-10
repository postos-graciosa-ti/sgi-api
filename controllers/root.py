from sqlmodel import Session, select

from database.sqlite import engine
from models.user import User


def handle_get_docs_info():
    return {"docs": "acess /docs", "redocs": "access /redocs"}


def handle_activate_render_server():
    with Session(engine) as session:
        has_users = session.exec(select(User)).all()

        result = bool(has_users)

        return result
