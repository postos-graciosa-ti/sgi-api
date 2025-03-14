from sqlmodel import Session, select

from database.sqlite import engine
from models.neighborhoods import Neighborhoods


def seed_neighborhoods():
    neighborhoods = [
        (1, "Adhemar Garcia"),
        (2, "América"),
        (3, "Anita Garibaldi"),
        (4, "Atiradores"),
        (5, "Aventureiro"),
        (6, "Boa Vista"),
        (7, "Boehmerwald"),
        (8, "Bom Retiro"),
        (9, "Bucarein"),
        (10, "Centro"),
        (11, "Comasa"),
        (12, "Costa e Silva"),
        (13, "Dona Francisca"),
        (14, "Espinheiros"),
        (15, "Fátima"),
        (16, "Floresta"),
        (17, "Glória"),
        (18, "Guanabara"),
        (19, "Iririú"),
        (20, "Itaum"),
        (21, "Itinga"),
        (22, "Jardim Iririú"),
        (23, "Jardim Paraíso"),
        (24, "Jardim Sofia"),
        (25, "Jarivatuba"),
        (26, "João Costa"),
        (27, "Morro do Meio"),
        (28, "Nova Brasília"),
        (29, "Paranaguamirim"),
        (30, "Parque Guarani"),
        (31, "Petrópolis"),
        (32, "Pirabeiraba"),
        (33, "Profipo"),
        (34, "Rio Bonito"),
        (35, "Saguaçu"),
        (36, "Santa Catarina"),
        (37, "Santo Antônio"),
        (38, "São Marcos"),
        (39, "Ulysses Guimarães"),
        (40, "Vila Cubatão"),
        (41, "Vila Nova"),
        (42, "Zona Industrial Norte"),
        (43, "Zona Industrial Tupy"),
    ]

    with Session(engine) as session:
        for id, name in neighborhoods:
            exist_neighborhood = session.exec(
                select(Neighborhoods).where(Neighborhoods.id == id)
            ).first()

            if not exist_neighborhood:
                neighborhood = Neighborhoods(id=id, name=name)

                session.add(neighborhood)

        session.commit()
