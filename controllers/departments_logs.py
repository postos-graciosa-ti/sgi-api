from sqlmodel import Session, select

from database.sqlite import engine
from models.department_logs import DepartmentsLogs


def handle_get_departments_logs(id: int):
    with Session(engine) as session:
        query = select(DepartmentsLogs).where(DepartmentsLogs.subsidiarie_id == id)

        departments_logs = session.exec(query).all()

        return departments_logs


def handle_post_departments_logs(id: int, department_logs_input: DepartmentsLogs):
    with Session(engine) as session:
        department_logs_input.subsidiarie_id = id

        session.add(department_logs_input)

        session.commit()

        session.refresh(department_logs_input)

        return department_logs_input
