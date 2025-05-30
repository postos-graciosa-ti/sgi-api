from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function


def handle_get_functions_by_subsidiarie(id: int):
    with Session(engine) as session:
        query = select(Function).where(Function.subsidiarie_id == id)

        functions = session.exec(query).all()

        return functions


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
    with Session(engine) as session:
        session.add(function)

        session.commit()

        session.refresh(function)

        return function


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

            db_function.cbo = function.cbo if function.cbo else db_function.cbo

            db_function.general_function_code = function.general_function_code

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
