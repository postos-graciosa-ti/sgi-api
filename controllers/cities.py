from sqlmodel import Session, select

from database.sqlite import engine
from models.cities import Cities
from pyhints.cities import GetCitiesOutput


async def handle_get_cities():
    with Session(engine) as session:
        cities = session.exec(select(Cities)).all()

        return [GetCitiesOutput(label=city.name, value=city.id) for city in cities]


async def handle_get_cities_by_id(id: int):
    with Session(engine) as session:
        city = session.exec(select(Cities).where(Cities.id == id)).one()

        return city
