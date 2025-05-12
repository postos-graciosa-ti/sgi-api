from sqlmodel import Session, select

from database.sqlite import engine
from models.applicants import Applicants
from models.function import Function


def handle_get_applicants():
    with Session(engine) as session:
        applicants = (
            session.exec(
                select(Applicants, Function).join(
                    Function, Applicants.desired_function == Function.id
                )
            )
            .mappings()
            .all()
        )

        return applicants


def handle_post_applicant(applicant: Applicants):
    with Session(engine) as session:
        session.add(applicant)

        session.commit()

        session.refresh(applicant)

        return applicant
