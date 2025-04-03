from sqlmodel import Session, select

from database.sqlite import engine
from models.applicants import Applicants


def handle_get_applicant():
    with Session(engine) as session:
        applicants = session.exec(select(Applicants)).all()

        return applicants


def handle_post_applicant(applicant: Applicants):
    with Session(engine) as session:
        session.add(applicant)

        session.commit()

        session.refresh(applicant)

        return applicant
