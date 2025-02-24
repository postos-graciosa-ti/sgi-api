from sqlmodel import Session, select

from database.sqlite import engine
from models.cities import Cities
from models.states import States


def handle_get_states():
    with Session(engine) as session:
        states = session.exec(select(States)).all()

        return [{"label": state.name, "value": state.id} for state in states]


def handle_get_states_by_id(id: int):
    with Session(engine) as session:
        state = session.exec(select(States).where(States.id == id)).all()

        return state


def handle_get_cities():
    with Session(engine) as session:
        cities = session.exec(select(Cities)).all()

        return [{"label": city.name, "value": city.id} for city in cities]


def handle_get_city_by_id(id: int):
    with Session(engine) as session:
        city = session.exec(select(Cities).where(Cities.id == id)).one()

        return city
