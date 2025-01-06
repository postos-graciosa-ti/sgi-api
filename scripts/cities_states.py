import httpx
from sqlmodel import Session, select
from database.sqlite import engine
from models.states import States
from models.cities import Cities


def get_states_from_ibge():
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados"

    with httpx.Client() as client:
        response = client.get(url)

    states_data = response.json()

    with Session(engine) as session:
        for state in states_data:
            state = States(name=state["nome"], sail=state["sigla"])

            session.add(state)

        session.commit()


def get_cities_from_ibge():
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/distritos"

    with httpx.Client() as client:
        response = client.get(url)

    cities_data = response.json()

    with Session(engine) as session:
        for city in cities_data:
            city = Cities(name=city["nome"])

            session.add(city)

        session.commit()
