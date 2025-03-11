from sqlmodel import Session, select

from database.sqlite import engine
from models.candidate_status import CandidateStatus


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
