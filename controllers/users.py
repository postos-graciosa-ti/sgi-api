from sqlmodel import Session, select
from database.sqlite import engine
from models.function import Function
from models.role import Role
from models.subsidiarie import Subsidiarie
from models.user import User
from repository.functions import create, update, delete
import json
from passlib.hash import pbkdf2_sha256
from fastapi import HTTPException


def handle_user_login(user: User):
    with Session(engine) as session:
        statement = select(User).where(User.email == user.email).limit(1)

        db_user = session.exec(statement).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        if not pbkdf2_sha256.verify(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Senha incorreta")

        return db_user


def handle_get_users():
    with Session(engine) as session:
        statement = (
            select(
                User.id,
                User.name,
                User.email,
                User.subsidiaries_id,
                Role.id.label("role_id"),
                Role.name.label("role_name"),
                Function.id.label("function_id"),
                Function.name.label("function_name"),
            )
            .join(Role, User.role_id == Role.id)
            .join(Function, User.function_id == Function.id)
        )

        users = session.exec(statement).all()

        all_subsidiaries = session.exec(select(Subsidiarie.id, Subsidiarie.name)).all()

        subsidiaries_map = {sub.id: sub.name for sub in all_subsidiaries}

        result = []

        for user in users:
            subsidiary_ids = json.loads(user[3])

            subsidiaries = [
                {"id": sub_id, "name": subsidiaries_map.get(sub_id, "Unknown")}
                for sub_id in subsidiary_ids
            ]

            result.append(
                {
                    "user_id": user[0],
                    "user_name": user[1],
                    "user_email": user[2],
                    "subsidiaries": subsidiaries,
                    "role_id": user[4],
                    "role_name": user[5],
                    "function_id": user[6],
                    "function_name": user[7],
                }
            )

    return result


def handle_post_user(user: User):
    result = create(user)

    return result


def handle_put_user(id: int, user: User):
    with Session(engine) as session:
        # Fetch user by id
        statement = select(User).where(User.id == id)
        db_user = session.execute(statement).scalars().first()

        if db_user:
            # Update user details
            db_user.name = user.name
            session.commit()  # Commit changes

            return db_user
        else:
            return None  # User not found


def handle_delete_user(id: int):
    result = delete(id, User)

    return result
