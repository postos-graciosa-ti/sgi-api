from sqlmodel import Session, select

from database.sqlite import engine
from models.cities import Cities
from models.states import States


def seed_cities():
    cities = [
        {"name": "Joinville", "state": "Santa Catarina"},
        {"name": "Florianópolis", "state": "Santa Catarina"},
        {"name": "Blumenau", "state": "Santa Catarina"},
        {"name": "Chapecó", "state": "Santa Catarina"},
        {"name": "Itajaí", "state": "Santa Catarina"},
        {"name": "Lages", "state": "Santa Catarina"},
        {"name": "Criciúma", "state": "Santa Catarina"},
        {"name": "São José", "state": "Santa Catarina"},
        {"name": "Jaraguá do Sul", "state": "Santa Catarina"},
        {"name": "Balneário Camboriú", "state": "Santa Catarina"},
    ]

    with Session(engine) as session:
        for city in cities:
            state = session.exec(
                select(States).where(States.name == city["state"])
            ).first()

            session.add(Cities(name=city["name"], state_id=state.id))

        session.commit()
