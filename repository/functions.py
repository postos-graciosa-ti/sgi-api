from sqlmodel import Session, select, text
from database.sqlite import engine


def find_all(Model: dict):
    with Session(engine) as session:
        statement = select(Model)

        rows = session.exec(statement).all()

    return rows


def create(formData: dict):
    with Session(engine) as session:
        session.add(formData)

        session.commit()

        session.refresh(formData)
    return formData


def update(id: int, Model: dict, formData: dict):
    with Session(engine) as session:
        statement = select(Model).where(Model.id == id)

        row = session.exec(statement).first()

        row = formData

        session.commit()

        session.refresh(row)
    return row


def delete(id: int, Model: dict):
    with Session(engine) as session:
        statement = select(Model).where(Model.id == id)

        row = session.exec(statement).first()

        session.delete(row)

        session.commit()

    return {"message": "Registro deletado com sucesso"}
  