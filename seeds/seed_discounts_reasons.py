from sqlmodel import Session, select

from database.sqlite import engine
from models.banks import Banks
from models.discount_reasons import DiscountReasons


def seed_discounts_reasons():
    discounts_reasons = [
        DiscountReasons(
            name="Erros Operacionais", description="Erros ocorridos em pista"
        ),
        DiscountReasons(
            name="Adiantamento de Salário",
            description="Adiantamentos do valor salarial",
        ),
        DiscountReasons(name="Farmácia", description="Descontos em função de farmácia"),
        DiscountReasons(
            name="Adiantamento de Salário",
            description="Adiantamentos do valor salarial",
        ),
        DiscountReasons(
            name="Odontologia",
            description="Descontos em função de odontologia",
        ),
        DiscountReasons(
            name="Psicóloga",
            description="Descontos em função de psicóloga",
        ),
        DiscountReasons(
            name="Nutricionista",
            description="Descontos em função de nutricionista",
        ),
    ]

    with Session(engine) as session:
        has_discounts_reasons = session.exec(select(DiscountReasons)).first()

        if not has_discounts_reasons:
            session.add_all(discounts_reasons)

            session.commit()
