from sqlmodel import Session, select

from database.sqlite import engine
from models.states import States
from pyhints.states import GetStatesOutput


async def handle_get_states():
    with Session(engine) as session:
        states = session.exec(select(States)).all()

        return [GetStatesOutput(label=state.name, value=state.id) for state in states]


async def handle_get_states_by_id(id: int):
    with Session(engine) as session:
        state = session.exec(select(States).where(States.id == id)).all()

        return state
