from sqlmodel import Session, select

from database.sqlite import engine
from models.neighborhoods import Neighborhoods


def handle_get_neighborhoods():
    with Session(engine) as session:
        neighborhoods = session.exec(select(Neighborhoods)).all()

        return neighborhoods


def handle_get_neighborhood_by_id(id: int):
    with Session(engine) as session:
        neighborhood = session.get(Neighborhoods, id)

        return neighborhood


def handle_get_neighborhoods_by_city(id: int):
    with Session(engine) as session:
        neighborhoods = session.exec(
            select(Neighborhoods).where(Neighborhoods.city_id == id)
        ).all()

        return neighborhoods


def handle_post_neighborhood(neighborhood: Neighborhoods):
    with Session(engine) as session:
        session.add(neighborhood)

        session.commit()

        session.refresh(neighborhood)

        return neighborhood


def handle_put_neighborhood(id: int, neighborhood: Neighborhoods):
    with Session(engine) as session:
        db_neighborhood = session.exec(
            select(Neighborhoods).where(Neighborhoods.id == id)
        ).one()

        if neighborhood is not None and neighborhood.name != db_neighborhood.name:
            db_neighborhood.name = neighborhood.name

        if (
            neighborhood.city_id is not None
            and neighborhood.city_id != db_neighborhood.city_id
        ):
            db_neighborhood.city_id = neighborhood.city_id

        session.add(db_neighborhood)

        session.commit()

        session.refresh(db_neighborhood)

        return db_neighborhood


def handle_delete_neighborhood(neighborhood_id: int):
    with Session(engine) as session:
        neighborhood = session.get(Neighborhoods, neighborhood_id)

        session.delete(neighborhood)

        session.commit()

        return {"message": "Neighborhood deleted successfully"}
