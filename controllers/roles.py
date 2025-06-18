from sqlmodel import Session, select

from database.sqlite import engine
from models.role import Role


def handle_get_roles():
    with Session(engine) as session:
        roles = session.exec(select(Role)).all()

        return roles


def handle_get_roles_by_id(id: int):
    with Session(engine) as session:
        role = session.exec(select(Role).where(Role.id == id)).first()

        return role
