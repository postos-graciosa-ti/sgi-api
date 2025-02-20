from sqlmodel import Session, select

from database.sqlite import engine
from models.cost_center import CostCenter


def handle_get_cost_center():
    with Session(engine) as session:
        cost_centers = session.exec(select(CostCenter)).all()

        return cost_centers


async def handle_get_cost_center_by_id(id: int):
    with Session(engine) as session:
        cost_center = session.get(CostCenter, id)

        return cost_center


async def handle_post_cost_center(cost_center_input: CostCenter):
    with Session(engine) as session:
        session.add(cost_center_input)

        session.commit()

        session.refresh(cost_center_input)

        return cost_center_input


async def handle_put_cost_center(id: int, cost_center_input: CostCenter):
    with Session(engine) as session:
        cost_center = session.get(CostCenter, id)

        cost_center.name = (
            cost_center_input.name if cost_center_input.name else cost_center.name
        )

        cost_center.description = (
            cost_center_input.description
            if cost_center_input.description
            else cost_center.description
        )

        session.add(cost_center)

        session.commit()

        session.refresh(cost_center)

        return cost_center


async def handle_delete_cost_center(id: int):
    with Session(engine) as session:
        cost_center = session.get(CostCenter, id)

        session.delete(cost_center)

        session.commit()

        return {"success": True}
