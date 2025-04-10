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
        {"name": "Moema", "city": "São Paulo"},
        {"name": "Itaim Bibi", "city": "São Paulo"},
        {"name": "Pinheiros", "city": "São Paulo"},
        {"name": "Vila Mariana", "city": "São Paulo"},
        {"name": "Tatuapé", "city": "São Paulo"},
        {"name": "Bela Vista", "city": "São Paulo"},
        {"name": "Copacabana", "city": "Rio de Janeiro"},
        {"name": "Ipanema", "city": "Rio de Janeiro"},
        {"name": "Barra da Tijuca", "city": "Rio de Janeiro"},
        {"name": "Leblon", "city": "Rio de Janeiro"},
        {"name": "Botafogo", "city": "Rio de Janeiro"},
        {"name": "Savassi", "city": "Belo Horizonte"},
        {"name": "Pampulha", "city": "Belo Horizonte"},
        {"name": "Lourdes", "city": "Belo Horizonte"},
        {"name": "Barreiro", "city": "Belo Horizonte"},
        {"name": "Centro", "city": "Belo Horizonte"},
        {"name": "Batel", "city": "Curitiba"},
        {"name": "Centro Cívico", "city": "Curitiba"},
        {"name": "Água Verde", "city": "Curitiba"},
        {"name": "Santa Felicidade", "city": "Curitiba"},
        {"name": "Boa Vista", "city": "Curitiba"},
        {"name": "Moinhos de Vento", "city": "Porto Alegre"},
        {"name": "Petrópolis", "city": "Porto Alegre"},
        {"name": "Cidade Baixa", "city": "Porto Alegre"},
        {"name": "Menino Deus", "city": "Porto Alegre"},
        {"name": "Centro Histórico", "city": "Porto Alegre"},
        {"name": "Barra", "city": "Salvador"},
        {"name": "Ondina", "city": "Salvador"},
        {"name": "Pituba", "city": "Salvador"},
        {"name": "Itapuã", "city": "Salvador"},
        {"name": "Rio Vermelho", "city": "Salvador"},
        {"name": "Boa Viagem", "city": "Recife"},
        {"name": "Casa Forte", "city": "Recife"},
        {"name": "Pina", "city": "Recife"},
        {"name": "Espinheiro", "city": "Recife"},
        {"name": "Santo Amaro", "city": "Recife"},
        {"name": "Aldeota", "city": "Fortaleza"},
        {"name": "Meireles", "city": "Fortaleza"},
        {"name": "Centro", "city": "Fortaleza"},
        {"name": "Parquelândia", "city": "Fortaleza"},
        {"name": "Mucuripe", "city": "Fortaleza"},
        {"name": "Centro", "city": "Florianópolis"},
        {"name": "Trindade", "city": "Florianópolis"},
        {"name": "Ingleses", "city": "Florianópolis"},
        {"name": "Campeche", "city": "Florianópolis"},
        {"name": "Lagoa da Conceição", "city": "Florianópolis"},
    ]

    with Session(engine) as session:
        for neighborhood in neighborhoods:
            city = session.exec(
                select(Cities).where(Cities.name == neighborhood["city"])
            ).first()

            if city:
                session.add(Neighborhoods(name=neighborhood["name"], city_id=city.id))

        session.commit()
