from sqlmodel import Session, select

from database.sqlite import engine


def get_record_by_column(model, column_name, column_value, quantity):
    with Session(engine) as session:
        if quantity == "single":
            column = getattr(model, column_name)

            result = session.exec(select(model).where(column == column_value)).first()

            return result

        elif quantity == "multiple":
            column = getattr(model, column_name)

            result = session.exec(select(model).where(column == column_value)).all()

            return result
