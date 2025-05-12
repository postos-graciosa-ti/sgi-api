from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, create_engine, event, text
from sqlmodel import Session, select

from database.sqlite import engine
from models.applicants import Applicants
from models.function import Function
from models.workers import Workers
from pyhints.applicants import RecruitProps

# applicants


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


def handle_patch_applicants(id: int, applicant: Applicants):
    with Session(engine) as session:
        db_applicant = session.exec(
            select(Applicants).where(Applicants.id == id)
        ).first()

        db_applicant.nature = (
            applicant.nature if applicant.nature else db_applicant.nature
        )

        db_applicant.how_long = (
            applicant.how_long if applicant.how_long else db_applicant.how_long
        )

        db_applicant.experience_function = (
            applicant.experience_function
            if applicant.experience_function
            else db_applicant.experience_function
        )

        db_applicant.redirect_to = (
            applicant.redirect_to if applicant.redirect_to else db_applicant.redirect_to
        )

        db_applicant.coordinator_observation = (
            applicant.coordinator_observation
            if applicant.coordinator_observation
            else db_applicant.coordinator_observation
        )

        session.add(db_applicant)

        session.commit()

        session.refresh(db_applicant)

        return db_applicant


def handle_delete_applicants(id: int):
    with Session(engine) as session:
        db_applicant = session.exec(
            select(Applicants).where(Applicants.id == id)
        ).first()

        session.delete(db_applicant)

        session.commit()

        return {"success": True}


# hire applicants


def handle_post_hire_applicants(recruit: RecruitProps):
    with Session(engine) as session:
        worker = Workers(**recruit.worker_data)

        admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d").date()

        worker.first_review_date = (admission_date + relativedelta(months=1)).strftime(
            "%Y-%m-%d"
        )
        worker.second_review_date = (admission_date + relativedelta(months=2)).strftime(
            "%Y-%m-%d"
        )

        session.add(worker)

        session.commit()

        session.refresh(worker)

        applicant = session.exec(
            select(Applicants).where(Applicants.id == recruit.applicant_id)
        ).first()

        session.delete(applicant)

        session.commit()

        return worker


# applicants notifications


def handle_get_applicants_notifications(id: int):
    with Session(engine) as session:
        query = text(
            """
            SELECT *
            FROM applicants
            WHERE redirect_to = :user_id
              AND (coordinator_observation IS NULL OR coordinator_observation = '')
            """
        )

        result = session.exec(query.params(user_id=id)).mappings().all()

        return result
