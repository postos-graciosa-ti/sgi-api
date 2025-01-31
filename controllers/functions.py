from sqlmodel import Session, select, text

from database.sqlite import engine
from models.function import Function
from repository.functions import create


def handle_get_functions():
    with Session(engine) as session:
        functions = session.exec(select(Function)).all()
    return functions


def handle_get_functions_for_users():
    with Session(engine) as session:
        functions = session.exec(select(Function)).all()

        target_names = {"Gerente", "Coordenador", "Analista de RH", "Analista de TI"}

        functions_for_users = [
            function for function in functions if function.name in target_names
        ]

        return functions_for_users


def handle_get_functions_for_workers():
    with Session(engine) as session:
        functions = session.exec(select(Function)).all()

        target_names = {"Frentista", "Caixa", "Trocador de óleo"}

        functions_for_workers = [
            function for function in functions if function.name in target_names
        ]

        return functions_for_workers


def handle_post_function(function: Function):
    result = create(function)

    return result


def handle_put_function(id: int, function: Function):
    with Session(engine) as session:
        db_function = session.exec(select(Function).where(Function.id == id)).first()

        if db_function:
            db_function.name = function.name if function.name else db_function.name

            db_function.description = (
                function.description
                if function.description
                else db_function.description
            )

            db_function.ideal_quantity = (
                function.ideal_quantity
                if function.ideal_quantity
                else db_function.ideal_quantity
            )

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
