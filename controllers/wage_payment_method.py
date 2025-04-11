from sqlmodel import Session, select

from database.sqlite import engine
from models.wage_payment_method import WagePaymentMethod


def handle_get_wage_payment_method():
    with Session(engine) as session:
        wage_payment_methods = session.exec(select(WagePaymentMethod)).all()

        return wage_payment_methods
