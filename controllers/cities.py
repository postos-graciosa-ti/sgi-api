from sqlmodel import Session, select

from database.sqlite import engine
from models.cities import Cities
from models.states import States
from pyhints.cities import GetCitiesOutput


def handle_get_cities():
    with Session(engine) as session:
        cities = (
            session.exec(
                select(Cities, States).join(States, Cities.state_id == States.id)
            )
            .mappings()
            .all()
        )

        return cities


def handle_get_city_by_id(id: int):
    with Session(engine) as session:
        cities = session.exec(select(Cities).where(Cities.id == id)).first()

        return cities


def handle_get_cities_by_state(id: int):
    with Session(engine) as session:
        cities = session.exec(select(Cities).where(Cities.state_id == id)).all()

        return cities


def handle_post_new_city(city: Cities):
    with Session(engine) as session:
        session.add(city)

        session.commit()

        session.refresh(city)

        return city


def handle_put_cities(id: int, city: Cities):
    with Session(engine) as session:
        db_city = session.exec(select(Cities).where(Cities.id == id)).first()

        db_city.name = city.name if city.name else db_city.name

        db_city.state_id = city.state_id if city.state_id else db_city.state_id

        session.add(db_city)

        session.commit()

        session.refresh(db_city)

        return db_city


def handle_delete_cities(id: int):
    with Session(engine) as session:
        db_city = session.exec(select(Cities).where(Cities.id == id)).first()

        session.delete(db_city)

        session.commit()

        return {"success": True}
