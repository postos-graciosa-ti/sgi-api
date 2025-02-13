from sqlmodel import Session, select

from database.sqlite import engine
from models.cost_center_logs import CostCenterLogs


async def handle_get_cost_center_logs(id: int):
    with Session(engine) as session:
        query = select(CostCenterLogs).where(CostCenterLogs.subsidiarie_id == id)

        costs_center_logs = session.exec(query).all()

        return costs_center_logs


async def handle_post_cost_center_logs(id: int, cost_center_log: CostCenterLogs):
    with Session(engine) as session:
        cost_center_log.subsidiarie_id = id

        session.add(cost_center_log)

        session.commit()

        session.refresh(cost_center_log)

        return cost_center_log
