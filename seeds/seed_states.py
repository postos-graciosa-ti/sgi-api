from sqlmodel import Session, select

from database.sqlite import engine
from models.nationalities import Nationalities
from models.states import States


def seed_brasil_states():
    states = [
        {"name": "Acre", "sail": "AC"},
        {"name": "Alagoas", "sail": "AL"},
        {"name": "Amapá", "sail": "AP"},
        {"name": "Amazonas", "sail": "AM"},
        {"name": "Bahia", "sail": "BA"},
        {"name": "Ceará", "sail": "CE"},
        {"name": "Distrito Federal", "sail": "DF"},
        {"name": "Espírito Santo", "sail": "ES"},
        {"name": "Goiás", "sail": "GO"},
        {"name": "Maranhão", "sail": "MA"},
        {"name": "Mato Grosso", "sail": "MT"},
        {"name": "Mato Grosso do Sul", "sail": "MS"},
        {"name": "Minas Gerais", "sail": "MG"},
        {"name": "Pará", "sail": "PA"},
        {"name": "Paraíba", "sail": "PB"},
        {"name": "Paraná", "sail": "PR"},
        {"name": "Pernambuco", "sail": "PE"},
        {"name": "Piauí", "sail": "PI"},
        {"name": "Rio de Janeiro", "sail": "RJ"},
        {"name": "Rio Grande do Norte", "sail": "RN"},
        {"name": "Rio Grande do Sul", "sail": "RS"},
        {"name": "Rondônia", "sail": "RO"},
        {"name": "Roraima", "sail": "RR"},
        {"name": "Santa Catarina", "sail": "SC"},
        {"name": "São Paulo", "sail": "SP"},
        {"name": "Sergipe", "sail": "SE"},
        {"name": "Tocantins", "sail": "TO"},
    ]

    with Session(engine) as session:
        nationalitie = session.exec(
            select(Nationalities).where(Nationalities.name == "Brasileiro")
        ).first()

        for state in states:
            session.add(
                States(
                    name=state["name"],
                    sail=state["sail"],
                    nationalities_id=nationalitie.id,
                )
            )

            session.commit()


def seed_venezuela_states():
    estados_venezuela = [
        {"name": "Amazonas", "sail": "AMA"},
        {"name": "Anzoátegui", "sail": "ANZ"},
        {"name": "Apure", "sail": "APU"},
        {"name": "Aragua", "sail": "ARA"},
        {"name": "Barinas", "sail": "BAR"},
        {"name": "Bolívar", "sail": "BOL"},
        {"name": "Carabobo", "sail": "CAR"},
        {"name": "Cojedes", "sail": "COJ"},
        {"name": "Delta Amacuro", "sail": "DEL"},
        {"name": "Falcón", "sail": "FAL"},
        {"name": "Guárico", "sail": "GUA"},
        {"name": "Lara", "sail": "LAR"},
        {"name": "Mérida", "sail": "MER"},
        {"name": "Miranda", "sail": "MIR"},
        {"name": "Monagas", "sail": "MON"},
        {"name": "Nueva Esparta", "sail": "NUE"},
        {"name": "Portuguesa", "sail": "POR"},
        {"name": "Sucre", "sail": "SUC"},
        {"name": "Táchira", "sail": "TAC"},
        {"name": "Trujillo", "sail": "TRU"},
        {"name": "Vargas", "sail": "VAR"},
        {"name": "Yaracuy", "sail": "YAR"},
        {"name": "Zulia", "sail": "ZUL"},
        {"name": "Distrito Capital", "sail": "DC"},
    ]

    with Session(engine) as session:
        nationalitie = session.exec(
            select(Nationalities).where(Nationalities.name == "Venezuelano")
        ).first()

        for estado in estados_venezuela:
            state = States(
                name=estado["name"],
                sail=estado["sail"],
                nationalities_id=nationalitie.id,
            )
            session.add(state)
        session.commit()
