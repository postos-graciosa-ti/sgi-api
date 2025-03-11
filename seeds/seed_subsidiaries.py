from sqlmodel import Session, select

from database.sqlite import engine
from models.subsidiarie import Subsidiarie


def seed_subsidiaries():
    with Session(engine) as session:
        existing_subsidiaries = session.exec(select(Subsidiarie)).all()

        if not existing_subsidiaries:
            subsidiaries = [
                Subsidiarie(
                    name="Posto Graciosa - Matriz",
                    cnpj="76.608.660/0001-11",
                    adress="R. Florianópolis, 510 – Itaum, Joinville – SC, 89207-000",
                    phone="(47) 3436-0030",
                    email="matriz@postosgraciosa.com.br",
                    coordinator=3,
                    manager=2,
                ),
                Subsidiarie(
                    name="Auto Posto Fátima",
                    cnpj="79.270.211/0001-02",
                    adress="R. Fátima, 1730 – Fátima, Joinville – SC, 89229-102",
                    phone="(47) 3466-0248",
                    email="fatima@postosgraciosa.com.br",
                    coordinator=4,
                ),
                Subsidiarie(
                    name="Posto Bemer",
                    cnpj="81.512.683/0001-68",
                    adress="R. Boehmerwald, 675 – Boehmerwald, Joinville – SC, 89232-485",
                    phone="(47) 3465-0328",
                    email="bemer@postosgraciosa.com.br",
                    coordinator=5,
                ),
                Subsidiarie(
                    name="Posto Jariva",
                    cnpj="04.123.127/0001-59",
                    adress="R. Monsenhor Gercino, 5085 – Jarivatuba, Joinville – SC, 89230-290",
                    phone="(47) 3466-4665",
                    email="jariva@postosgraciosa.com.br",
                    coordinator=6,
                    manager=2,
                ),
                Subsidiarie(
                    name="Posto Graciosa V",
                    cnpj="84.708.437/0006-89",
                    adress="R. Santa Catarina, 1870 – Floresta, Joinville – SC, 89212-000",
                    phone="(47) 3436-1763",
                    email="graciosav@postosgraciosa.com.br",
                    coordinator=7,
                    manager=2,
                ),
                Subsidiarie(
                    name="Auto Posto Piraí",
                    cnpj="11.168.652/0001-56",
                    adress="R. Quinze de Novembro, 5031 – Vila Nova, Joinville – SC, 89237-000",
                    phone="(47) 3422-9676",
                    email="pirai@postosgraciosa.com.br",
                    coordinator=8,
                    manager=2,
                ),
            ]

            session.add_all(subsidiaries)

            session.commit()
