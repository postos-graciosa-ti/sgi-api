from sqlmodel import Session, select

from database.sqlite import engine
from functions.logs import log_action


def patch_record(
    model,
    pk_column,
    pk_column_value,
    updates: dict,
    request=None,
    user=None,
):
    with Session(engine) as session:
        pk = getattr(model, pk_column)

        instance = session.exec(select(model).where(pk == pk_column_value)).first()

        if not instance:
            return {"error": "Record not found"}

        before_state = instance.dict()

        for column, value in updates.items():
            if value is not None:
                setattr(instance, column, value)

        session.add(instance)

        session.commit()

        session.refresh(instance)

        if request and user:
            log_action(
                action="patch",
                table_name=getattr(model, "__tablename__", model.__name__.lower()),
                record_id=pk_column_value,
                user_id=user["id"],
                details={
                    "before": before_state,
                    "after": instance.dict(),
                },
                endpoint=str(request.url.path),
            )

        return instance
