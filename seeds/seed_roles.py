from sqlmodel import Session, select

from database.sqlite import engine
from models.role import Role


def seed_roles():
    with Session(engine) as session:
        existing_roles = session.exec(select(Role)).all()

        if not existing_roles:
            roles = [Role(name="Administrador"), Role(name="Usuário")]

            session.add_all(roles)

            session.commit()
