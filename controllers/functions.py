from sqlmodel import Session, select, text

from database.sqlite import engine
from models.function import Function
from repository.functions import create


def handle_get_functions():
    with Session(engine) as session:
        functions = session.exec(select(Function)).all()
    return functions


def handle_post_function(function: Function):
    result = create(function)

    return result


def handle_put_function(id: int, function: Function):
    with Session(engine) as session:
        statement = select(Function).where(Function.id == id)

        db_function = session.exec(statement).first()

        db_function.name = function.name

        db_function.description = function.description

        session.add(db_function)

        session.commit()

        session.refresh(db_function)

        return db_function


def handle_delete_function(id: int):
    with Session(engine) as session:
        statement = select(Function).where(Function.id == id)

        db_function = session.exec(statement).first()

        session.delete(db_function)

        session.commit()

        return db_function
