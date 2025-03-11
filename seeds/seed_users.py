from passlib.hash import pbkdf2_sha256
from sqlmodel import Session, select

from database.sqlite import engine
from models.user import User


def seed_users():
    with Session(engine) as session:
        existing_users = session.exec(select(User)).all()

        if not existing_users:
            users = [
                User(
                    email="dev@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Dev",
                    role_id=1,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                    phone="(47) 99688-4562",
                ),
                User(
                    email="michel@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Michel",
                    role_id=1,
                    is_active=True,
                    subsidiaries_id="[1,4,5,6]",
                    phone="(47) 99100-3040",
                ),
                User(
                    email="nilson@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Nilson",
                    role_id=2,
                    is_active=True,
                    subsidiaries_id="[1]",
                    phone="(47) 99137-7949",
                ),
                User(
                    email="daniel@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Daniel",
                    role_id=2,
                    is_active=True,
                    subsidiaries_id="[2]",
                    phone="(47)",
                ),
                User(
                    email="rudinick@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Rudinick",
                    role_id=2,
                    is_active=True,
                    subsidiaries_id="[3]",
                    phone="(47)",
                ),
                User(
                    email="marcia@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Marcia",
                    role_id=2,
                    is_active=True,
                    subsidiaries_id="[4]",
                    phone="(47) 99195-9966",
                ),
                User(
                    email="thiago@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Thiago",
                    role_id=2,
                    is_active=True,
                    subsidiaries_id="[5]",
                    phone="(47) 98841-4102",
                ),
                User(
                    email="gisele@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Gisele",
                    role_id=2,
                    is_active=True,
                    subsidiaries_id="[6]",
                    phone="(47) 98459-9344",
                ),
            ]

            session.add_all(users)

            session.commit()
