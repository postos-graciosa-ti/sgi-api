from sqlmodel import Session

from database.sqlite import engine
from models.genders import Genders


def seed_genders():
    genders = [
        Genders(name="Masculino"),
        Genders(name="Feminino"),
        Genders(name="Não-binário"),
        Genders(name="Gênero fluido"),
        Genders(name="Agênero"),
        Genders(name="Bigênero"),
        Genders(name="Pangênero"),
        Genders(name="Outro"),
        Genders(name="Prefiro não informar"),
    ]

    with Session(engine) as session:
        session.add_all(genders)

        session.commit()
