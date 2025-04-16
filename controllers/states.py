from sqlmodel import Session, select

from database.sqlite import engine
from models.nationalities import Nationalities
from models.states import States
from pyhints.states import GetStatesOutput


def handle_get_states():
    with Session(engine) as session:
        get_states = select(States, Nationalities).join(
            Nationalities, States.nationalities_id == Nationalities.id
        )

        db_results = session.exec(get_states).all()

        result = []

        for state, nationalitie in db_results:
            result.append(
                {
                    "id": state.id,
                    "name": state.name,
                    "sail": state.sail,
                    "nationalitie_id": nationalitie.id,
                    "nationalitie_name": nationalitie.name,
                }
            )

        return result


def handle_get_states_by_id(id: int):
    with Session(engine) as session:
        state = session.exec(select(States).where(States.id == id)).first()

        return state


def handle_get_states_by_nationalitie(id: int):
    with Session(engine) as session:
        states_by_nationalitie = session.exec(
            select(States).where(States.nationalities_id == id)
        ).all()

        return states_by_nationalitie


def handle_post_states(state: States):
    with Session(engine) as session:
        session.add(state)

        session.commit()

        session.refresh(state)

        return state


def handle_put_states(id: int, state: States):
    with Session(engine) as session:
        db_state = session.exec(select(States).where(States.id == id)).first()

        db_state.name = state.name if state.name else db_state.name

        db_state.sail = state.sail if state.sail else db_state.sail

        db_state.nationalities_id = (
            state.nationalities_id
            if state.nationalities_id
            else db_state.nationalities_id
        )

        session.add(db_state)

        session.commit()

        session.refresh(db_state)

        return db_state


def handle_delete_states(id: int):
    with Session(engine) as session:
        db_state = session.exec(select(States).where(States.id == id)).first()

        session.delete(db_state)

        session.commit()

        return {"success": True}
