from sqlmodel import Session, select

from database.sqlite import engine


def delete_record(model, pk_column, pk_column_value):
    with Session(engine) as session:
        model_pk = getattr(model, pk_column)

        db_record = session.exec(
            select(model).where(model_pk == pk_column_value)
        ).first()

        session.delete(db_record)

        session.commit()

        return {"success": True}
