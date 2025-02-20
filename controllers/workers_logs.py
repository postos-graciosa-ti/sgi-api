from sqlmodel import Session, select

from database.sqlite import engine
from models.user import User
from models.workers import Workers
from models.workers_logs import WorkersLogs
from models.workers_logs_create import WorkersLogsCreate
from models.workers_logs_delete import WorkersLogsDelete
from models.workers_logs_update import WorkersLogsUpdate
from pyhints.workers import (
    WorkerLogCreateInput,
    WorkerLogDeleteInput,
    WorkerLogUpdateInput,
)


def handle_get_create_workers_logs(id: int):
    with Session(engine) as session:
        statement = (
            select(WorkersLogsCreate, Workers, User)
            .join(Workers, WorkersLogsCreate.worker_id == Workers.id)
            .join(User, WorkersLogsCreate.user_id == User.id)
            .where(WorkersLogsCreate.subsidiarie_id == id)
            .order_by(WorkersLogsCreate.id.desc())
        )

        workers_create_logs = session.exec(statement).all()

        return [
            {
                "worker_id": log.WorkersLogsCreate.worker_id,
                "user_id": log.WorkersLogsCreate.user_id,
                "worker_name": log.Workers.name,
                "user_name": log.User.name,
                "created_at": log.WorkersLogsCreate.created_at,
                "created_at_time": log.WorkersLogsCreate.created_at_time,
            }
            for log in workers_create_logs
        ]


def handle_post_create_workers_logs(id: int, worker_log: WorkerLogCreateInput):
    with Session(engine) as session:
        worker_log = WorkersLogsCreate(
            subsidiarie_id=id,
            created_at=worker_log.created_at,
            created_at_time=worker_log.created_at_time,
            user_id=worker_log.user_id,
            worker_id=worker_log.worker_id,
        )

        session.add(worker_log)

        session.commit()

        session.refresh(worker_log)

        return worker_log


def handle_get_update_workers_logs(id: int):
    with Session(engine) as session:
        statement = (
            select(WorkersLogsUpdate, Workers, User)
            .join(Workers, WorkersLogsUpdate.worker_id == Workers.id)
            .join(User, WorkersLogsUpdate.user_id == User.id)
            .where(WorkersLogsUpdate.subsidiarie_id == id)
            .order_by(WorkersLogsUpdate.id.desc())
        )

        workers_update_logs = session.exec(statement).all()

        return [
            {
                "worker_id": log.WorkersLogsUpdate.worker_id,
                "user_id": log.WorkersLogsUpdate.user_id,
                "worker_name": log.Workers.name,
                "user_name": log.User.name,
                "updated_at": log.WorkersLogsUpdate.updated_at,
                "updated_at_time": log.WorkersLogsUpdate.updated_at_time,
            }
            for log in workers_update_logs
        ]


def handle_post_update_workers_logs(id: int, worker_log: WorkerLogUpdateInput):
    with Session(engine) as session:
        worker_log = WorkersLogsUpdate(
            subsidiarie_id=id,
            updated_at=worker_log.updated_at,
            updated_at_time=worker_log.updated_at_time,
            user_id=worker_log.user_id,
            worker_id=worker_log.worker_id,
        )

        session.add(worker_log)

        session.commit()

        session.refresh(worker_log)

        return worker_log


def handle_get_delete_workers_logs(id: int):
    with Session(engine) as session:
        statement = (
            select(WorkersLogsDelete, Workers, User)
            .join(Workers, WorkersLogsDelete.worker_id == Workers.id)
            .join(User, WorkersLogsDelete.user_id == User.id)
            .where(WorkersLogsDelete.subsidiarie_id == id)
            .order_by(WorkersLogsDelete.id.desc())
        )

        workers_delete_logs = session.exec(statement).all()

        return [
            {
                "worker_id": log.WorkersLogsDelete.worker_id,
                "user_id": log.WorkersLogsDelete.user_id,
                "worker_name": log.Workers.name,
                "user_name": log.User.name,
                "deleted_at": log.WorkersLogsDelete.deleted_at,
                "deleted_at_time": log.WorkersLogsDelete.deleted_at_time,
            }
            for log in workers_delete_logs
        ]


def handle_post_delete_workers_logs(id: int, worker_log: WorkerLogDeleteInput):
    with Session(engine) as session:
        worker_log = WorkersLogsDelete(
            subsidiarie_id=id,
            deleted_at=worker_log.deleted_at,
            deleted_at_time=worker_log.deleted_at_time,
            user_id=worker_log.user_id,
            worker_id=worker_log.worker_id,
        )

        session.add(worker_log)

        session.commit()

        session.refresh(worker_log)

        return worker_log


def handle_get_workers_logs(id: int):
    with Session(engine) as session:
        query = select(WorkersLogs).where(WorkersLogs.subsidiarie_id == id)

        workers_logs = session.exec(query).all()

        return workers_logs


def handle_post_workers_logs(id: int, workers_log: WorkersLogs):
    with Session(engine) as session:
        workers_log.subsidiarie_id = id

        session.add(workers_log)

        session.commit()

        session.refresh(workers_log)

        return workers_log
