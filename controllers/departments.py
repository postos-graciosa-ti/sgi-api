from sqlmodel import Session, select

from database.sqlite import engine
from models.department import Department


async def handle_get_departments():
    with Session(engine) as session:
        departments = session.exec(select(Department)).all()

        return departments


async def handle_get_department_by_id(id: int):
    with Session(engine) as session:
        department = session.get(Department, id)

        return department


async def handle_post_department(department_input: Department):
    with Session(engine) as session:
        session.add(department_input)

        session.commit()

        session.refresh(department_input)

        return department_input


async def handle_put_department(id: int, department_input: Department):
    with Session(engine) as session:
        department = session.get(Department, id)

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

        return department


async def handle_delete_department(id: int):
    with Session(engine) as session:
        department = session.get(Department, id)

        session.delete(department)

        session.commit()

        return {"success": True}
