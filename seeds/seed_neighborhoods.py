from sqlmodel import Session, select

from database.sqlite import engine
from models.cities import Cities
from models.neighborhoods import Neighborhoods


def seed_neighborhoods():
    neighborhoods = [
        {"name": "Itaum", "city": "Joinville"},
        {"name": "Centro", "city": "Joinville"},
        {"name": "Boa Vista", "city": "Joinville"},
        {"name": "Comasa", "city": "Joinville"},
        {"name": "Aventureiro", "city": "Joinville"},
        {"name": "Costa e Silva", "city": "Joinville"},
        {"name": "Iririú", "city": "Joinville"},
        {"name": "Saguaçu", "city": "Joinville"},
        {"name": "Petrópolis", "city": "Joinville"},
        {"name": "Santo Antônio", "city": "Joinville"},
        {"name": "Jarivatuba", "city": "Joinville"},
        {"name": "Santa Catarina", "city": "Joinville"},
        {"name": "Boehmerwald", "city": "Joinville"},
        {"name": "Koch", "city": "Joinville"},
        {"name": "Vila Nova", "city": "Joinville"},
        {"name": "São Marcos", "city": "Joinville"},
        {"name": "Anita Garibaldi", "city": "Joinville"},
        {"name": "Floresta", "city": "Joinville"},
        {"name": "Ponta Aguda", "city": "Joinville"},
        {"name": "Atiradores", "city": "Joinville"},
        {"name": "Zanellato", "city": "Joinville"},
        {"name": "Pirabeiraba", "city": "Joinville"},
        {"name": "João Costa", "city": "Joinville"},
        {"name": "Bela Vista", "city": "Joinville"},
        {"name": "Bairro das Nações", "city": "Joinville"},
        {"name": "Chico de Paula", "city": "Joinville"},
        {"name": "Estrada da Ribeira", "city": "Joinville"},
        {"name": "Serraria", "city": "Joinville"},
        {"name": "Cohab", "city": "Joinville"},
    ]

    with Session(engine) as session:
        for neighborhood in neighborhoods:
            city = session.exec(
                select(Cities).where(Cities.name == neighborhood["city"])
            ).first()

            session.add(Neighborhoods(name=neighborhood["name"], city_id=city.id))

        session.commit()
