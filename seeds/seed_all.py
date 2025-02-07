from datetime import time

from passlib.hash import pbkdf2_sha256
from sqlmodel import Session, select

from database.sqlite import engine
from models.candidate_status import CandidateStatus
from models.cost_center import CostCenter
from models.department import Department
from models.function import Function
from models.month import Month
from models.resignable_reasons import ResignableReasons
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
                    # function_id=1,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="regiane@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Regiane",
                    role_id=1,
                    # function_id=1,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="mauricio@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Mauricio",
                    role_id=1,
                    # function_id=4,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="mariele@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Mariele",
                    role_id=1,
                    # function_id=4,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="thiago@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Thiago",
                    role_id=1,
                    # function_id=5,
                    is_active=True,
                    subsidiaries_id="[1,2,3,4,5,6]",
                ),
                User(
                    email="michel@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Michel",
                    role_id=1,
                    # function_id=2,
                    is_active=True,
                    subsidiaries_id="[1,4,5,6]",
                ),
                User(
                    email="nilson@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Nilson",
                    role_id=2,
                    # function_id=3,
                    is_active=True,
                    subsidiaries_id="[1]",
                ),
                User(
                    email="daniel@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Daniel",
                    role_id=2,
                    # function_id=3,
                    is_active=True,
                    subsidiaries_id="[2]",
                ),
                User(
                    email="rudinick@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Rudinick",
                    role_id=2,
                    # function_id=3,
                    is_active=True,
                    subsidiaries_id="[3]",
                ),
                User(
                    email="marcia@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Marcia",
                    role_id=2,
                    # function_id=3,
                    is_active=True,
                    subsidiaries_id="[4]",
                ),
                User(
                    email="tiago@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Tiago",
                    role_id=2,
                    # function_id=3,
                    is_active=True,
                    subsidiaries_id="[5]",
                ),
                User(
                    email="luciano@gmail.com",
                    password=pbkdf2_sha256.hash("teste"),
                    name="Luciano",
                    role_id=2,
                    # function_id=3,
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
                    end_time=time(14, 0),
                    end_interval_time=time(11, 0),
                ),
                Turn(
                    name="Tarde",
                    start_time=time(14, 0),
                    start_interval_time=time(18, 0),
                    end_time=time(22, 0),
                    end_interval_time=time(19, 0),
                ),
                Turn(
                    name="Noite",
                    start_time=time(22, 0),
                    start_interval_time=time(2, 0),
                    end_time=time(6, 0),
                    end_interval_time=time(3, 0),
                ),
                Turn(
                    name="Volante",
                    start_time=time(0, 0),
                    start_interval_time=time(0, 0),
                    end_time=time(0, 0),
                    end_interval_time=time(0, 0),
                ),
                Turn(
                    name="Comercial",
                    start_time=time(8, 0),
                    start_interval_time=time(12, 0),
                    end_time=time(18, 0),
                    end_interval_time=time(13, 0),
                ),
                Turn(
                    name="Meia madrugada",
                    start_time=time(18, 0),
                    start_interval_time=time(0, 0),
                    end_time=time(0, 0),
                    end_interval_time=time(13, 0),
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
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Frentista 02",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=1,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Frentista 03",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=2,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Frentista 04",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=2,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Frentista 05",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=3,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Frentista 06",
                    subsidiarie_id=1,
                    function_id=6,
                    turn_id=3,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Caixa 01",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=1,
                    is_active=True,
                    cost_center_id=1,
                    department_id=2,
                ),
                Workers(
                    name="Caixa 02",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=1,
                    is_active=True,
                    cost_center_id=1,
                    department_id=2,
                ),
                Workers(
                    name="Caixa 03",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=2,
                    is_active=True,
                    cost_center_id=1,
                    department_id=2,
                ),
                Workers(
                    name="Caixa 04",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=2,
                    is_active=True,
                    cost_center_id=1,
                    department_id=2,
                ),
                Workers(
                    name="Caixa 05",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=3,
                    is_active=True,
                    cost_center_id=1,
                    department_id=2,
                ),
                Workers(
                    name="Caixa 06",
                    subsidiarie_id=1,
                    function_id=7,
                    turn_id=3,
                    is_active=True,
                    cost_center_id=1,
                    department_id=2,
                ),
                Workers(
                    name="Trocador de óleo 01",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=1,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Trocador de óleo 02",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=1,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Trocador de óleo 03",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=2,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Trocador de óleo 04",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=2,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Trocador de óleo 05",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=3,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
                Workers(
                    name="Trocador de óleo 06",
                    subsidiarie_id=1,
                    function_id=8,
                    turn_id=3,
                    is_active=True,
                    cost_center_id=1,
                    department_id=1,
                ),
            ]

            session.add_all(workers)

            session.commit()


def create_cost_centers():
    cost_centers = [
        {"name": "Vendas", "description": "Departamento de Vendas"},
        {"name": "Administrativo", "description": "Departamento Administrativo"},
        {"name": "Serviços Gerais", "description": "Departamento de Serviços Gerais"},
    ]

    with Session(engine) as session:
        for center in cost_centers:
            cost_center = CostCenter(
                name=center["name"], description=center["description"]
            )

            session.add(cost_center)

        session.commit()


def create_departments():
    departments = [
        {"name": "Pista", "description": "Setor de Pista"},
        {
            "name": "Loja de Conveniência",
            "description": "Setor da Loja de Conveniência",
        },
        {"name": "Compras", "description": "Setor de Compras"},
        {"name": "Comercial", "description": "Setor Comercial"},
        {"name": "Serviços Gerais", "description": "Setor de Serviços Gerais"},
        {"name": "Administrativo", "description": "Setor Administrativo"},
        {"name": "Recursos Humanos", "description": "Setor de Recursos Humanos"},
        {"name": "Financeiro", "description": "Setor Financeiro"},
    ]

    with Session(engine) as session:
        for department in departments:
            department_instance = Department(
                name=department["name"], description=department["description"]
            )

            session.add(department_instance)

        session.commit()


def demission_reasons():
    resignable_reasons = [
        {
            "name": "Demissão sem Justa Causa",
            "description": "Rescisão sem motivo específico por parte da empresa.",
        },
        {
            "name": "Demissão por Justa Causa",
            "description": "Rescisão devido a falta grave cometida pelo empregado.",
        },
        {
            "name": "Pedido de Demissão",
            "description": "Solicitação do empregado para encerrar o contrato de trabalho.",
        },
        {
            "name": "Pedido de Demissão Antecipada do Contrato de Experiência (parte empregado)",
            "description": "O empregado solicita o fim do contrato antes do prazo.",
        },
        {
            "name": "Demissão Antecipada do Contrato de Experiência (parte empresa)",
            "description": "A empresa decide encerrar o contrato de experiência antes do prazo.",
        },
        {
            "name": "Demissão por Justa Causa",
            "description": "Rescisão por justa causa devido a conduta inapropriada do empregado.",
        },
    ]

    with Session(engine) as session:
        for resignable_reason in resignable_reasons:
            reason = ResignableReasons(
                name=resignable_reason["name"],
                description=resignable_reason["description"],
            )

            session.add(reason)

        session.commit()


def seed_database():
    demission_reasons()
    seed_roles()
    seed_subsidiaries()
    seed_candidate_status()
    seed_months()
    create_cost_centers()
    create_departments()
    seed_users()
