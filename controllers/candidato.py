from datetime import datetime

from sqlmodel import Session, select, text

from database.sqlite import engine
from models.candidato import Candidato


def handle_get_candidato():
    with Session(engine) as session:
        statement = select(Candidato)

        candidatos = session.exec(statement).all()
    return candidatos


def handle_get_candidato_by_id(id: int):
    with Session(engine) as session:
        statement = select(Candidato).where(Candidato.id == id)

        candidato = session.exec(statement).first()
    return candidato


def handle_post_candidato(candidato: Candidato):
    # convertendo as datas para o tipo date do python
    candidato.data_cadastro = datetime.strptime(
        candidato.data_cadastro, "%d/%m/%Y"
    ).date()

    candidato.data_nascimento = datetime.strptime(
        candidato.data_nascimento, "%d/%m/%Y"
    ).date()

    candidato.ultima_data_admissão = datetime.strptime(
        candidato.ultima_data_admissão, "%d/%m/%Y"
    ).date()

    candidato.ultima_data_demissão = datetime.strptime(
        candidato.ultima_data_demissão, "%d/%m/%Y"
    ).date()

    candidato.ultima_penultima_data_admissão = datetime.strptime(
        candidato.ultima_penultima_data_admissão, "%d/%m/%Y"
    ).date()

    candidato.ultima_penultima_data_demissão = datetime.strptime(
        candidato.ultima_penultima_data_demissão, "%d/%m/%Y"
    ).date()

    candidato.ultima_ante_penultima_data_admissão = datetime.strptime(
        candidato.ultima_ante_penultima_data_admissão, "%d/%m/%Y"
    ).date()

    candidato.ultima_ante_penultima_data_demissão = datetime.strptime(
        candidato.ultima_ante_penultima_data_demissão, "%d/%m/%Y"
    ).date()

    candidato.data_encaminhamento_segunda_entrevista = datetime.strptime(
        candidato.data_encaminhamento_segunda_entrevista, "%d/%m/%Y"
    ).date()

    candidato.data_encaminhamento_admissao = datetime.strptime(
        candidato.data_encaminhamento_admissao, "%d/%m/%Y"
    ).date()

    candidato.data_prevista_admissao = datetime.strptime(
        candidato.data_prevista_admissao, "%d/%m/%Y"
    ).date()

    # salvando no banco de dados
    with Session(engine) as session:
        session.add(candidato)

        session.commit()

        session.refresh(candidato)
    return candidato


def handle_delete_candidato(id: int):
    with Session(engine) as session:
        statement = select(Candidato).where(Candidato.id == id)

        candidato = session.exec(statement).first()

        session.delete(candidato)

        session.commit()

        if candidato:
            return {"mensagem": "Candidato excluído com sucesso"}
        else:
            return {"mensagem": "Candidato não encontrado"}
