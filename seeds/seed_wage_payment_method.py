from sqlmodel import Session, select

from database.sqlite import engine
from models.wage_payment_method import WagePaymentMethod


def seed_wage_payment_methods():
    wage_payment_methods = [
        WagePaymentMethod(name="Dinheiro"),
        WagePaymentMethod(name="Cheque"),
    ]

    with Session(engine) as session:
        has_wage_payment_method = session.exec(select(WagePaymentMethod)).first()

        if not has_wage_payment_method:
            session.add_all(wage_payment_methods)

            session.commit()
