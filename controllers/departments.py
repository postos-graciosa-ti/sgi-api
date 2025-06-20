from fastapi import Request
from sqlmodel import Session, select

from database.sqlite import engine
from functions.auth import AuthUser
from functions.logs import log_action
from models.department import Department


def handle_get_departments():
    with Session(engine) as session:
        departments = session.exec(select(Department)).all()

        return departments


def handle_get_department_by_id(id: int):
    with Session(engine) as session:
        department = session.get(Department, id)

        return department


def handle_post_department(request, department_input: Department, user: AuthUser):
    with Session(engine) as session:
        session.add(department_input)

        session.commit()

        session.refresh(department_input)

        log_action(
            action="post",
            table_name="departments",
            record_id=department_input.id,
            user_id=user["id"],
            details={
                "before": None,
                "after": department_input.dict(),
            },
            endpoint=str(request.url.path),
        )

        return department_input


def handle_put_department(
    request: Request, id: int, department_input: Department, user: AuthUser
):
    with Session(engine) as session:
        department = session.get(Department, id)

        before_data = department

        department.name = (
            department_input.name if department_input.name else department.name
        )

        department.description = (
            department_input.description
            if department_input.description
            else department.description
        )

        session.add(department)

        session.commit()

        session.refresh(department)

        log_action(
            action="put",
            table_name="departments",
            record_id=department_input.id,
            user_id=user["id"],
            details={
                "before": before_data.dict(),
                "after": department_input.dict(),
            },
            endpoint=str(request.url.path),
        )

        return department


def handle_delete_department(request: Request, id: int, user: AuthUser):
    with Session(engine) as session:
        department = session.get(Department, id)

        before_data = department

        session.delete(department)

        session.commit()

        log_action(
            action="delete",
            table_name="departments",
            record_id=before_data.id,
            user_id=user["id"],
            details={
                "before": before_data.dict(),
                "after": None,
            },
            endpoint=str(request.url.path),
        )

        return {"success": True}
