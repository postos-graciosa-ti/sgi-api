from sqlmodel import Session, select

from database.sqlite import engine
from models.cities import Cities
from models.states import States


def seed_brasil_cities():
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
        {"name": "São Paulo", "state": "São Paulo"},
        {"name": "Campinas", "state": "São Paulo"},
        {"name": "Santos", "state": "São Paulo"},
        {"name": "São Bernardo do Campo", "state": "São Paulo"},
        {"name": "Ribeirão Preto", "state": "São Paulo"},
        {"name": "Rio de Janeiro", "state": "Rio de Janeiro"},
        {"name": "Niterói", "state": "Rio de Janeiro"},
        {"name": "Duque de Caxias", "state": "Rio de Janeiro"},
        {"name": "Nova Iguaçu", "state": "Rio de Janeiro"},
        {"name": "Campos dos Goytacazes", "state": "Rio de Janeiro"},
        {"name": "Belo Horizonte", "state": "Minas Gerais"},
        {"name": "Uberlândia", "state": "Minas Gerais"},
        {"name": "Contagem", "state": "Minas Gerais"},
        {"name": "Juiz de Fora", "state": "Minas Gerais"},
        {"name": "Betim", "state": "Minas Gerais"},
        {"name": "Curitiba", "state": "Paraná"},
        {"name": "Londrina", "state": "Paraná"},
        {"name": "Maringá", "state": "Paraná"},
        {"name": "Ponta Grossa", "state": "Paraná"},
        {"name": "Cascavel", "state": "Paraná"},
        {"name": "Porto Alegre", "state": "Rio Grande do Sul"},
        {"name": "Caxias do Sul", "state": "Rio Grande do Sul"},
        {"name": "Pelotas", "state": "Rio Grande do Sul"},
        {"name": "Canoas", "state": "Rio Grande do Sul"},
        {"name": "Santa Maria", "state": "Rio Grande do Sul"},
        {"name": "Salvador", "state": "Bahia"},
        {"name": "Feira de Santana", "state": "Bahia"},
        {"name": "Vitória da Conquista", "state": "Bahia"},
        {"name": "Camaçari", "state": "Bahia"},
        {"name": "Itabuna", "state": "Bahia"},
        {"name": "Recife", "state": "Pernambuco"},
        {"name": "Jaboatão dos Guararapes", "state": "Pernambuco"},
        {"name": "Olinda", "state": "Pernambuco"},
        {"name": "Caruaru", "state": "Pernambuco"},
        {"name": "Petrolina", "state": "Pernambuco"},
        {"name": "Fortaleza", "state": "Ceará"},
        {"name": "Caucaia", "state": "Ceará"},
        {"name": "Juazeiro do Norte", "state": "Ceará"},
        {"name": "Maracanaú", "state": "Ceará"},
        {"name": "Sobral", "state": "Ceará"},
    ]

    with Session(engine) as session:
        for city in cities:
            state = session.exec(
                select(States).where(States.name == city["state"])
            ).first()

            if state:
                session.add(Cities(name=city["name"], state_id=state.id))

        session.commit()


def seed_venezuela_cities():
    cidades_por_estado = {
        "Amazonas": ["Puerto Ayacucho"],
        "Anzoátegui": ["Barcelona", "Puerto La Cruz", "El Tigre"],
        "Apure": ["San Fernando de Apure"],
        "Aragua": ["Maracay", "La Victoria"],
        "Barinas": ["Barinas"],
        "Bolívar": ["Ciudad Bolívar", "Ciudad Guayana"],
        "Carabobo": ["Valencia", "Puerto Cabello"],
        "Cojedes": ["San Carlos"],
        "Delta Amacuro": ["Tucupita"],
        "Falcón": ["Coro", "Punto Fijo"],
        "Guárico": ["San Juan de los Morros"],
        "Lara": ["Barquisimeto", "Carora"],
        "Mérida": ["Mérida", "El Vigía"],
        "Miranda": ["Los Teques", "Guarenas", "Guatire"],
        "Monagas": ["Maturín"],
        "Nueva Esparta": ["La Asunción", "Porlamar"],
        "Portuguesa": ["Guanare", "Acarigua"],
        "Sucre": ["Cumaná", "Carúpano"],
        "Táchira": ["San Cristóbal"],
        "Trujillo": ["Trujillo", "Valera"],
        "Vargas": ["La Guaira"],
        "Yaracuy": ["San Felipe"],
        "Zulia": ["Maracaibo", "Cabimas"],
        "Distrito Capital": ["Caracas"],
    }

    with Session(engine) as session:
        for estado_nome, cidades in cidades_por_estado.items():
            statement = select(States).where(States.name == estado_nome)

            estado = session.exec(statement).first()

            if estado:
                for cidade in cidades:
                    city = Cities(name=cidade, state_id=estado.id)

                    session.add(city)

        session.commit()
