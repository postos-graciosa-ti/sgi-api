from sqlmodel import Session, select

from database.sqlite import engine
from models.function import Function
from models.open_positions import OpenPositions
from models.subsidiarie import Subsidiarie
from models.turn import Turn


def handle_get_open_positions():
    with Session(engine) as session:
        open_positions = session.exec(select(OpenPositions)).all()

        result = [
            {
                "id": open_position.id,
                "subsidiarie": session.get(Subsidiarie, open_position.subsidiarie_id),
                "function": session.get(Function, open_position.function_id),
                "turn": session.get(Turn, open_position.turn_id),
            }
            for open_position in open_positions
        ]

        return result


def handle_get_open_positions_by_subsidiarie(id: int):
    with Session(engine) as session:
        open_positions = session.exec(
            select(OpenPositions).where(OpenPositions.subsidiarie_id == id)
        ).all()

        result = [
            {
                "subsidiarie": session.get(Subsidiarie, open_position.subsidiarie_id),
                "function": session.get(Function, open_position.function_id),
                "turn": session.get(Turn, open_position.turn_id),
            }
            for open_position in open_positions
        ]

        return result


def handle_post_open_positions(open_position: OpenPositions):
    with Session(engine) as session:
        session.add(open_position)

        session.commit()

        session.refresh(open_position)

        return {"success": True}


def handle_delete_open_positions(id: int):
    with Session(engine) as session:
        db_open_position = session.exec(
            select(OpenPositions).where(OpenPositions.id == id)
        ).first()

        session.delete(db_open_position)

        session.commit()

        return {"success": True}
