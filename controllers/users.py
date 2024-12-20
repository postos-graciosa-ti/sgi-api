import json

from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function
from models.role import Role
from models.subsidiarie import Subsidiarie
from models.user import User
from pyhints.users import GetUserRoles, Test, VerifyEmail, ConfirmPassword
from repository.functions import create, delete, update


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
        statement = select(User).where(User.id == id)

        db_user = session.exec(statement).first()

        db_user.email = user.email

        db_user.name = user.name

        db_user.role_id = user.role_id

        db_user.subsidiaries_id = user.subsidiaries_id

        db_user.function_id = user.function_id

        db_user.is_active = user.is_active

        session.add(db_user)

        session.commit()

        session.refresh(db_user)

    return db_user


def handle_delete_user(id: int):
    result = delete(id, User)

    return result


def handle_get_users_roles():
    with Session(engine) as session:
        statement = select(
            User.id,
            User.name,
            User.email,
            Role.name,
        ).join(Role, User.role_id == Role.id, isouter=True)

        results = session.exec(statement)

        users = [
            GetUserRoles(
                id=result[0],
                name=result[1],
                email=result[2],
                role=result[3],
            )
            for result in results
        ]

        return users


def handle_get_user_by_id(id: int):
    with Session(engine) as session:
        user = session.get(User, id)
    return user


def handle_get_test(arr: Test):
    user_subsidiaries = eval(arr.arr)

    subsidiaries_array = []

    for subsidiary_id in user_subsidiaries:
        with Session(engine) as session:
            statement = select(Subsidiarie).where(Subsidiarie.id == subsidiary_id)

            subsidiary = session.exec(statement).first()

        subsidiaries_array.append(subsidiary)

    return subsidiaries_array


def handle_verify_email(userData: VerifyEmail):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == userData.email)).first()

    if user:
        return {"status": "true", "message": "Email existe no banco de dados."}
    else:
        return {"status": "false", "message": "Email não encontrado no banco de dados."}


def handle_confirm_password(userData: ConfirmPassword):
    with Session(engine) as session:
        statement = select(User).where(User.email == userData.email)

        results = session.exec(statement)

        user = results.one()

        user.password = pbkdf2_sha256.hash(userData.password)

        session.add(user)

        session.commit()

        session.refresh(user)

        return user
