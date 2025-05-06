import json
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from jose import jwt
from passlib.hash import pbkdf2_sha256
from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function
from models.role import Role
from models.subsidiarie import Subsidiarie
from models.user import User
from pyhints.users import (
    ChangeUserPasswordInput,
    ConfirmPassword,
    CreateUserPasswordInput,
    GetUserRoles,
    Test,
    VerifyEmail,
)

load_dotenv()

secret = os.environ.get("SECRET")

algorithm = os.environ.get("ALGORITHM")


def handle_user_login(user: User):
    with Session(engine) as session:
        statement = select(User).where(User.email == user.email).limit(1)

        db_user = session.exec(statement).first()

        if not db_user:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        if not pbkdf2_sha256.verify(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        payload = {"id": db_user.id, "email": db_user.email}

        token = jwt.encode(payload, secret, algorithm)

        db_user_subsidiaries_ids = json.loads(db_user.subsidiaries_id)

        if not db_user_subsidiaries_ids:
            raise HTTPException(status_code=400, detail="Erro ao processar filiais")

        user_subsidiaries = []

        for subsidiarie_id in db_user_subsidiaries_ids:
            user_subsidiarie = session.get(Subsidiarie, subsidiarie_id)

            if user_subsidiarie:
                user_subsidiaries.append(
                    {"label": user_subsidiarie.name, "value": user_subsidiarie.id}
                )

        return JSONResponse(
            {
                "data": {
                    "id": db_user.id,
                    "email": db_user.email,
                    "name": db_user.name,
                    "role_id": db_user.role_id,
                    "subsidiaries_id": db_user.subsidiaries_id,
                    "user_subsidiaries": user_subsidiaries,
                    "function_id": db_user.function_id,
                    "is_active": db_user.is_active,
                },
                "token": token,
            }
        )


# def handle_get_users():
#     with Session(engine) as session:
#         statement = (
#             select(
#                 User.id,
#                 User.name,
#                 User.email,
#                 User.subsidiaries_id,
#                 Role.id.label("role_id"),
#                 Role.name.label("role_name"),
#                 Function.id.label("function_id"),
#                 Function.name.label("function_name"),
#             )
#             .join(Role, User.role_id == Role.id)
#             .join(Function, User.function_id == Function.id)
#         )

#         users = session.exec(statement).all()

#         all_subsidiaries = session.exec(select(Subsidiarie.id, Subsidiarie.name)).all()

#         subsidiaries_map = {sub.id: sub.name for sub in all_subsidiaries}

#         result = []

#         for user in users:
#             subsidiary_ids = json.loads(user[3])

#             subsidiaries = [
#                 {"id": sub_id, "name": subsidiaries_map.get(sub_id, "Unknown")}
#                 for sub_id in subsidiary_ids
#             ]

#             result.append(
#                 {
#                     "user_id": user[0],
#                     "user_name": user[1],
#                     "user_email": user[2],
#                     "subsidiaries": subsidiaries,
#                     "role_id": user[4],
#                     "role_name": user[5],
#                     "function_id": user[6],
#                     "function_name": user[7],
#                 }
#             )

#     return result


def handle_post_user(user: User):
    with Session(engine) as session:
        session.add(user)

        session.commit()

        session.refresh(user)

        return user


def handle_put_user(id: int, user: User):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)

        db_user = session.exec(statement).first()

        db_user.email = user.email if user.email else db_user.email

        db_user.name = user.name if user.name else db_user.name

        db_user.role_id = user.role_id if user.role_id else db_user.role_id

        db_user.subsidiaries_id = (
            user.subsidiaries_id if user.subsidiaries_id else db_user.subsidiaries_id
        )

        db_user.function_id = (
            user.function_id if user.function_id else db_user.function_id
        )

        db_user.is_active = user.is_active if user.is_active else db_user.is_active

        db_user.phone = user.phone if user.phone else db_user.phone

        session.add(db_user)

        session.commit()

        session.refresh(db_user)

    return db_user


def handle_delete_user(id: int):
    with Session(engine) as session:
        user = session.get(User, id)

        session.delete(user)

        session.commit()

        return {"status": "ok"}


def handle_get_users_roles():
    with Session(engine) as session:
        statement = select(User.id, User.name, User.email, Role.name, User.phone).join(
            Role, User.role_id == Role.id, isouter=True
        )

        results = session.exec(statement)

        users = [
            GetUserRoles(
                id=result[0],
                name=result[1],
                email=result[2],
                role=result[3],
                phone=result[4],
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


def handle_get_users():
    with Session(engine) as session:
        users = (
            session.exec(select(User, Role).join(Role, User.role_id == Role.id))
            .tuples()
            .all()
        )

        result = []

        for user, role in users:
            subsidiary_ids = []

            if user.subsidiaries_id:
                try:
                    subsidiary_ids = json.loads(user.subsidiaries_id)

                except json.JSONDecodeError:
                    subsidiary_ids = []

            result.append(
                {
                    "user_id": user.id,
                    "user_email": user.email,
                    "user_name": user.name,
                    "user_subsidiaries": [
                        session.get(Subsidiarie, id)
                        for id in subsidiary_ids
                        if id is not None and session.get(Subsidiarie, id) is not None
                    ],
                    "role_id": role.id,
                    "role_name": role.name,
                    "user_phone": user.phone,
                }
            )

    return result


def handle_verify_email(userData: VerifyEmail):
    with Session(engine) as session:
        user = session.exec(
            select(User)
            .where(User.email == userData.email)
            .where(User.password == None)
        ).first()

    if user:
        return {"status": "true", "message": "Email existe no banco de dados."}
    else:
        return {"status": "false", "message": "Email não encontrado no banco de dados."}


def handle_create_user_password(userData: CreateUserPasswordInput):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == userData.email)).first()

        userHasPassword = bool(user.password)

        if userHasPassword:
            raise HTTPException(status_code=400, detail="Usuário já possui senha")
        else:
            user.password = pbkdf2_sha256.hash(userData.password)

            session.add(user)

            session.commit()

            session.refresh(user)

            db_user_subsidiaries_ids = json.loads(user.subsidiaries_id)

            user_subsidiaries = []

            for subsidiarie_id in db_user_subsidiaries_ids:
                user_subsidiarie = session.get(Subsidiarie, subsidiarie_id)

                if user_subsidiarie:
                    user_subsidiaries.append(
                        {"label": user_subsidiarie.name, "value": user_subsidiarie.id}
                    )

            payload = {"id": user.id, "email": user.email}

            token = jwt.encode(payload, secret, algorithm)

            return JSONResponse(
                {
                    "data": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "role_id": user.role_id,
                        "subsidiaries_id": user.subsidiaries_id,
                        "user_subsidiaries": user_subsidiaries,
                        "function_id": user.function_id,
                        "is_active": user.is_active,
                    },
                    "token": token,
                }
            )


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


def handle_change_password(userData: ChangeUserPasswordInput):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == userData.email)).first()

        if not pbkdf2_sha256.verify(userData.currentPassword, user.password):
            raise HTTPException(status_code=400, detail="Senha incorreta")

        user.password = pbkdf2_sha256.hash(userData.newPassword)

        session.add(user)

        session.commit()

        session.refresh(user)

    return user
