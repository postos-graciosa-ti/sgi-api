from sqlmodel import Session, select

from database.sqlite import engine
from functions.auth import AuthUser
from functions.logs import log_action
from models.nationalities import Nationalities


def handle_get_nationalities():
    with Session(engine) as session:
        nationalities = session.exec(select(Nationalities)).all()

        return nationalities


def handle_post_nationalities(request, nationalitie: Nationalities, user: AuthUser):
    with Session(engine) as session:
        session.add(nationalitie)

        session.commit()

        session.refresh(nationalitie)

        log_action(
            action="post",
            table_name="nationalities",
            record_id=nationalitie.id,
            user_id=user["id"],
            details={
                "before": None,
                "after": nationalitie.dict(),
            },
            endpoint=str(request.url.path),
        )

        return nationalitie


def handle_put_nationalities(request, id: int, nationalitie: Nationalities, user: dict):
    with Session(engine) as session:
        db_nationalitie = session.exec(
            select(Nationalities).where(Nationalities.id == id)
        ).first()

        log_action(
            action="put",
            table_name="nationalities",
            record_id=id,
            user_id=user["id"],
            details={
                "before": db_nationalitie.dict(),
                "after": nationalitie.dict(),
            },
            endpoint=str(request.url.path),
        )

        if nationalitie.name is not None:
            db_nationalitie.name = nationalitie.name

        session.add(db_nationalitie)

        session.commit()

        session.refresh(db_nationalitie)

        return db_nationalitie


def handle_delete_nationalities(request, id: int, user: dict):
    with Session(engine) as session:
        db_nationalitie = session.exec(
            select(Nationalities).where(Nationalities.id == id)
        ).first()

        log_action(
            action="delete",
            table_name="nationalities",
            record_id=id,
            user_id=user["id"],
            details={
                "before": db_nationalitie.dict(),
                "after": None,
            },
            endpoint=str(request.url.path),
        )

        session.delete(db_nationalitie)

        session.commit()

        return {"success": True}
