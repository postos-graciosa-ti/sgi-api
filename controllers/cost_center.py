from fastapi import Request
from sqlmodel import Session, select

from database.sqlite import engine
from functions.auth import AuthUser
from functions.logs import log_action
from models.cost_center import CostCenter


def handle_get_cost_center():
    with Session(engine) as session:
        cost_centers = session.exec(select(CostCenter)).all()

        return cost_centers


def handle_get_cost_center_by_id(id: int):
    with Session(engine) as session:
        cost_center = session.get(CostCenter, id)

        return cost_center


def handle_post_cost_center(
    request: Request, cost_center_input: CostCenter, user: AuthUser
):
    with Session(engine) as session:
        session.add(cost_center_input)

        session.commit()

        session.refresh(cost_center_input)

        log_action(
            action="post",
            table_name="cost_center",
            record_id=cost_center_input.id,
            user_id=user["id"],
            details={
                "before": None,
                "after": cost_center_input.dict(),
            },
            endpoint=str(request.url.path),
        )

        return cost_center_input


def handle_put_cost_center(
    request: Request, id: int, cost_center_input: CostCenter, user: AuthUser
):
    with Session(engine) as session:
        cost_center = session.get(CostCenter, id)

        before_data = cost_center

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

        log_action(
            action="put",
            table_name="cost_center",
            record_id=cost_center_input.id,
            user_id=user["id"],
            details={
                "before": before_data.dict(),
                "after": cost_center_input.dict(),
            },
            endpoint=str(request.url.path),
        )

        return cost_center


def handle_delete_cost_center(request: Request, id: int, user: AuthUser):
    with Session(engine) as session:
        cost_center = session.get(CostCenter, id)

        before_data = cost_center

        session.delete(cost_center)

        session.commit()

        log_action(
            action="put",
            table_name="cost_center",
            record_id=before_data.id,
            user_id=user["id"],
            details={
                "before": before_data.dict(),
                "after": None,
            },
            endpoint=str(request.url.path),
        )

        return {"success": True}
