from sqlmodel import Session

from database.sqlite import engine
from models.country import Country


def seed_countries():
    with Session(engine) as session:
        south_american_countries = [
            {"name": "Argentina"},
            {"name": "Brasil"},
            {"name": "Chile"},
            {"name": "Colômbia"},
            {"name": "Equador"},
            {"name": "Guiana"},
            {"name": "Paraguai"},
            {"name": "Peru"},
            {"name": "Suriname"},
            {"name": "Uruguai"},
            {"name": "Venezuela"},
        ]

        for country in south_american_countries:
            session.add(Country(name=Country["name"]))

        session.commit()
