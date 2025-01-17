from datetime import time

from passlib.hash import pbkdf2_sha256
from sqlmodel import Session, select

from database.sqlite import engine
from models.candidate_status import CandidateStatus
from models.function import Function
from models.month import Month
from models.role import Role
from models.subsidiarie import Subsidiarie
from models.turn import Turn
from models.user import User
from models.workers import Workers
from scripts.cities_states import get_cities_from_ibge, get_states_from_ibge


def seed_roles():
    with Session(engine) as session:
        existing_roles = session.exec(select(Role)).all()
        if not existing_roles:
            roles = [Role(name="Administrador"), Role(name="Usuário")]
            session.add_all(roles)
            session.commit()


def seed_subsidiaries():
    with Session(engine) as session:
        existing_subsidiaries = session.exec(select(Subsidiarie)).all()
        if not existing_subsidiaries:
            subsidiaries = [
                Subsidiarie(
                    name="Posto Graciosa - Matriz",
                    adress="R. Florianópolis, 510 – Itaum, Joinville – SC, 89207-000",
                    phone="(47) 3436-0030",
                    email="matriz@postosgraciosa.com.br",
                ),
                Subsidiarie(
                    name="Auto Posto Fátima",
                    adress="R. Fátima, 1730 – Fátima, Joinville – SC, 89229-102",
                    phone="(47) 3466-0248",
                    email="fatima@postosgraciosa.com.br",
                ),
                Subsidiarie(
                    name="Posto Bemer",
                    adress="R. Boehmerwald, 675 – Boehmerwald, Joinville – SC, 89232-485",
                    phone="(47) 3465-0328",
                    email="bemer@postosgraciosa.com.br",
                ),
                Subsidiarie(
                    name="Posto Jariva",
                    adress="R. Monsenhor Gercino, 5085 – Jarivatuba, Joinville – SC, 89230-290",
                    phone="(47) 3466-4665",
                    email="jariva@postosgraciosa.com.br",
                ),
                Subsidiarie(
                    name="Posto Graciosa V",
                    adress="R. Santa Catarina, 1870 – Floresta, Joinville – SC, 89212-000",
                    phone="(47) 3436-1763",
                    email="graciosav@postosgraciosa.com.br",
                ),
                Subsidiarie(
                    name="Auto Posto Piraí",
                    adress="R. Quinze de Novembro, 5031 – Vila Nova, Joinville – SC, 89237-000",
                    phone="(47) 3422-9676",
                    email="pirai@postosgraciosa.com.br",
                ),
            ]
            session.add_all(subsidiaries)
            session.commit()


def seed_candidate_status():
    with Session(engine) as session:
        existing_candidate_status = session.exec(select(CandidateStatus)).all()
        if not existing_candidate_status:
            candidate_status = [
                CandidateStatus(name="Cadastrado"),
                CandidateStatus(name="Primeira Entrevista"),
                CandidateStatus(name="Segunda Entrevista"),
                CandidateStatus(name="Aguardando Exame Médico"),
                CandidateStatus(name="Contratado"),
            ]
            session.add_all(candidate_status)
            session.commit()


def seed_users():
    with Session(engine) as session:
        existing_users = session.exec(select(User)).all()
        if not existing_users:
            users = [
                User(
                    email="admin@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Admin",
                    role_id=1,
                    function_id=1,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="regiane@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Regiane",
                    role_id=1,
                    function_id=1,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="mauricio@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Mauricio",
                    role_id=1,
                    function_id=4,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="mariele@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Mariele",
                    role_id=1,
                    function_id=4,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="thiago@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Thiago",
                    role_id=1,
                    function_id=5,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="michel@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Michel",
                    role_id=1,
                    function_id=2,
                    is_active=True,
                    subsidiaries_id="[1,4,5,6]",
                ),
                User(
                    email="nilson@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Nilson",
                    role_id=2,
                    function_id=3,
                    is_active=True,
                    subsidiaries_id="[1]",
                ),
                User(
                    email="daniel@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Daniel",
                    role_id=2,
                    function_id=3,
                    is_active=True,
                    subsidiaries_id="[2]",
                ),
                User(
                    email="rudinick@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Rudinick",
                    role_id=2,
                    function_id=3,
                    is_active=True,
                    subsidiaries_id="[3]",
                ),
                User(
                    email="marcia@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Marcia",
                    role_id=2,
                    function_id=3,
                    is_active=True,
                    subsidiaries_id="[4]",
                ),
                User(
                    email="tiago@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Tiago",
                    role_id=2,
                    function_id=3,
                    is_active=True,
                    subsidiaries_id="[5]",
                ),
                User(
                    email="luciano@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Luciano",
                    role_id=2,
                    function_id=3,
                    is_active=True,
                    subsidiaries_id="[6]",
                ),
            ]
            session.add_all(users)
            session.commit()


def seed_functions():
    with Session(engine) as session:
        existing_functions = session.exec(select(Function)).all()
        if not existing_functions:
            functions = [
                Function(
                    name="Diretor",
                    description="Diretor do posto de combustível",
                ),
                Function(
                    name="Gerente",
                    description="Gerente do posto de combustível",
                ),
                Function(
                    name="Coordenador",
                    description="Coordenador do posto de combustível",
                ),
                Function(
                    name="Analista de RH",
                    description="Analista de RH do posto de combustível",
                ),
                Function(
                    name="Analista de TI",
                    description="Analista de TI do posto de combustível",
                ),
                Function(
                    name="Frentista",
                    description="Atendimento ao cliente no posto de combustível",
                ),
                Function(
                    name="Caixa",
                    description="Responsável por realizar transações financeiras no caixa",
                ),
                Function(
                    name="Trocador de óleo",
                    description="Trocador de óleo do posto de combustível",
                ),
            ]
            session.add_all(functions)
            session.commit()


def seed_turns():
    with Session(engine) as session:
        existing_turns = session.exec(select(Turn)).all()
        if not existing_turns:
            turns = [
                Turn(
                    name="Manhã",
                    start_time=time(6, 0),
                    start_interval_time=time(10, 0),
                    end_time=time(11, 0),
                    end_interval_time=time(14, 0),
                ),
                Turn(
                    name="Tarde",
                    start_time=time(14, 0),
                    start_interval_time=time(18, 0),
                    end_time=time(19, 0),
                    end_interval_time=time(22, 0),
                ),
                Turn(
                    name="Noite",
                    start_time=time(22, 0),
                    start_interval_time=time(2, 0),
                    end_time=time(3, 0),
                    end_interval_time=time(6, 0),
                ),
                Turn(
                    name="Volante",
                    start_time=time(0, 0),
                    start_interval_time=time(0, 0),
                    end_time=time(0, 0),
                    end_interval_time=time(0, 0),
                ),
            ]

            session.add_all(turns)

            session.commit()


def seed_months():
    with Session(engine) as session:
        existing_months = session.exec(select(Month)).all()

        if not existing_months:
            months = [
                Month(id=1, name="janeiro"),
                Month(id=2, name="fevereiro"),
                Month(id=3, name="março"),
                Month(id=4, name="abril"),
                Month(id=5, name="maio"),
                Month(id=6, name="junho"),
                Month(id=7, name="julho"),
                Month(id=8, name="agosto"),
                Month(id=9, name="setembro"),
                Month(id=10, name="outubro"),
                Month(id=11, name="novembro"),
                Month(id=12, name="dezembro"),
            ]

            session.add_all(months)

            session.commit()


def seed_workers():
    with Session(engine) as session:
        existing_workers = session.exec(select(Workers)).all()

        if not existing_workers:
            workers = [
                Workers(
                    name="Frentista 01",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=1,
                    is_active=True,
                ),
                Workers(
                    name="Frentista 02",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=1,
                    is_active=True,
                ),
                Workers(
                    name="Frentista 03",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=2,
                    is_active=True,
                ),
                Workers(
                    name="Frentista 04",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=2,
                    is_active=True,
                ),
                Workers(
                    name="Frentista 05",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=3,
                    is_active=True,
                ),
                Workers(
                    name="Frentista 06",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=3,
                    is_active=True,
                ),
                Workers(
                    name="Caixa 01",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=1,
                    is_active=True,
                ),
                Workers(
                    name="Caixa 02",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=1,
                    is_active=True,
                ),
                Workers(
                    name="Caixa 03",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=2,
                    is_active=True,
                ),
                Workers(
                    name="Caixa 04",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=2,
                    is_active=True,
                ),
                Workers(
                    name="Caixa 05",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=3,
                    is_active=True,
                ),
                Workers(
                    name="Caixa 06",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=3,
                    is_active=True,
                ),
                Workers(
                    name="Trocador de óleo 01",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=1,
                    is_active=True,
                ),
                Workers(
                    name="Trocador de óleo 02",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=1,
                    is_active=True,
                ),
                Workers(
                    name="Trocador de óleo 03",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=2,
                    is_active=True,
                ),
                Workers(
                    name="Trocador de óleo 04",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=2,
                    is_active=True,
                ),
                Workers(
                    name="Trocador de óleo 05",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=3,
                    is_active=True,
                ),
                Workers(
                    name="Trocador de óleo 06",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=3,
                    is_active=True,
                ),
            ]

            session.add_all(workers)

            session.commit()


def seed_database():
    seed_roles()
    seed_subsidiaries()
    seed_candidate_status()
    seed_users()
    seed_functions()
    seed_turns()
    seed_months()
    seed_workers()

    get_states_from_ibge()
    get_cities_from_ibge()
