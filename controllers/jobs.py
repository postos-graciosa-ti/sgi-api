from sqlmodel import Session, select

from database.sqlite import engine
from models.jobs import Jobs


def handle_get_jobs():
    with Session(engine) as session:
        jobs = session.exec(select(Jobs)).all()
    return jobs


def handle_get_jobs_by_subsidiarie_id(subsidiarie_id):
    with Session(engine) as session:
        statement = select(Jobs).where(Jobs.subsidiarie_id == subsidiarie_id)

        jobs = session.exec(statement).all()
    return jobs


def handle_post_job(job: Jobs):
    with Session(engine) as session:
        session.add(job)
        session.commit()
        session.refresh(job)
    return job


def handle_delete_job(job_id):
    with Session(engine) as session:
        job = session.get(Jobs, job_id)

        if job:
            session.delete(job)

            session.commit()

    return {"message": "Job deleted successfully"}
