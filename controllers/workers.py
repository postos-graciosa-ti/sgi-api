from datetime import date, datetime, timedelta

from sqlmodel import Session, select, update

from database.sqlite import engine
from models.cities import Cities
from models.civil_status import CivilStatus
from models.cost_center import CostCenter
from models.department import Department
from models.function import Function
from models.genders import Genders
from models.jobs import Jobs
from models.neighborhoods import Neighborhoods
from models.resignable_reasons import ResignableReasons
from models.scale import Scale
from models.states import States
from models.turn import Turn
from models.workers import Workers
from models.workers_notations import WorkersNotations
from pyhints.scales import WorkerDeactivateInput
from pyhints.workers import PostWorkerNotationInput
from models.ethnicity import Ethnicity


def handle_get_worker_by_id(id: int):
    with Session(engine) as session:
        worker = session.exec(select(Workers).where(Workers.id == id)).one()

        return worker


def handle_get_workers_by_subsidiarie(subsidiarie_id: int):
    with Session(engine) as session:
        workers = session.exec(
            select(
                Workers.id,
                Workers.name,
                Workers.is_active,
                Workers.admission_date,
                Workers.resignation_date,
                Workers.resignation_reason_id,
                Workers.enrolment,
                Workers.sales_code,
                Workers.picture,
                Workers.timecode,
                Workers.first_review_date,
                Workers.second_review_date,
                Workers.esocial,
                Workers.gender_id,
                Workers.civil_status_id,
                Workers.street,
                Workers.street_number,
                Workers.street_complement,
                Workers.neighborhood_id,
                Workers.cep,
                Workers.city,
                Workers.state,
                Workers.phone,
                Workers.mobile,
                Workers.email,
                Workers.ethnicity_id,
                Workers.birthdate,
                Workers.birthcity,
                Workers.birthstate,
                Workers.fathername,
                Workers.mothername,
                Workers.cpf,
                Workers.rg,
                Workers.rg_issuing_agency,
                Workers.rg_state,
                Workers.rg_expedition_date,
                Workers.military_cert_number,
                Workers.pis,
                Workers.pis_register_date,
                Workers.votant_session,
                Workers.votant_title,
                Workers.votant_zone,
                Workers.ctps,
                Workers.ctps_serie,
                Workers.ctps_state,
                Workers.ctps_emission_date,
                Workers.cnh,
                Workers.cnh_category,
                Workers.cnh_emition_date,
                Workers.cnh_valid_date,
                Workers.first_job,
                Workers.was_employee,
                Workers.union_contribute_current_year,
                Workers.receiving_unemployment_insurance,
                Workers.previous_experience,
                Workers.month_wage,
                Workers.hour_wage,
                Workers.journey_wage,
                Workers.transport_voucher,
                Workers.transport_voucher_quantity,
                Workers.diary_workjourney,
                Workers.week_workjourney,
                Workers.month_workjourney,
                Workers.experience_time,
                Workers.nocturne_hours,
                Workers.dangerousness,
                Workers.unhealthy,
                Workers.wage_payment_method,
                Function.id.label("function_id"),
                Function.name.label("function_name"),
                Turn.id.label("turn_id"),
                Turn.name.label("turn_name"),
                Turn.start_time.label("turn_start_time"),
                Turn.end_time.label("turn_end_time"),
                CostCenter.id.label("cost_center_id"),
                CostCenter.name.label("cost_center"),
                Department.id.label("department_id"),
                Department.name.label("department"),
                ResignableReasons.id.label("resignation_reason_id"),
                ResignableReasons.name.label("resignation_reason_name"),
            )
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .join(Function, Function.id == Workers.function_id)
            .join(Turn, Workers.turn_id == Turn.id)
            .join(CostCenter, Workers.cost_center_id == CostCenter.id)
            .join(Department, Workers.department_id == Department.id)
            .join(
                ResignableReasons,
                ResignableReasons.id == Workers.resignation_reason_id,
                isouter=True,
            )
        ).all()

        return [
            {
                "worker_id": worker.id,
                "worker_name": worker.name,
                "worker_is_active": worker.is_active,
                "admission_date": worker.admission_date,
                "resignation_date": worker.resignation_date,
                "resignation_reason_id": worker.resignation_reason_id,
                "resignation_reason_name": worker.resignation_reason_name,
                "worker_enrolment": worker.enrolment,
                "worker_sales_code": worker.sales_code,
                "picture": worker.picture,
                "timecode": worker.timecode,
                "first_review_date": worker.first_review_date,
                "second_review_date": worker.second_review_date,
                "esocial": worker.esocial,
                "function_id": worker.function_id,
                "function_name": worker.function_name,
                "turn_id": worker.turn_id,
                "turn_name": worker.turn_name,
                "turn_start_time": worker.turn_start_time,
                "turn_end_time": worker.turn_end_time,
                "cost_center_id": worker.cost_center_id,
                "cost_center": worker.cost_center,
                "department_id": worker.department_id,
                "department": worker.department,
                "gender": session.get(Genders, worker.gender_id),
                "civil_status": session.get(CivilStatus, worker.civil_status_id),
                "street": worker.street,
                "street_number": worker.street_number,
                "street_complement": worker.street_complement,
                "neighborhood": session.get(Neighborhoods, worker.neighborhood_id),
                "cep": worker.cep,
                "city": session.get(Cities, worker.city),
                "state": session.get(States, worker.state),
                "phone": worker.phone,
                "mobile": worker.mobile,
                "email": worker.email,
                "ethnicity": session.get(Ethnicity, worker.ethnicity_id),
                "birthdate": worker.birthdate,
                "birthcity": session.get(Cities, worker.birthcity),
                "birthstate": session.get(States, worker.birthstate),
                "fathername": worker.fathername,
                "mothername": worker.mothername,
                "cpf": worker.cpf,
                "rg": worker.rg,
                "rg_issuing_agency": worker.rg_issuing_agency,
                "rg_state": worker.rg_state,
                "rg_expedition_date": worker.rg_expedition_date,
                "military_cert_number": worker.military_cert_number,
                "pis": worker.pis,
                "pis_register_date": worker.pis_register_date,
                "votant_title": worker.votant_title,
                "votant_zone": worker.votant_zone,
                "votant_session": worker.votant_session,
                "ctps": worker.ctps,
                "ctps_serie": worker.ctps_serie,
                "ctps_state": session.get(States, worker.ctps_state),
                "ctps_emission_date": worker.ctps_emission_date,
                "cnh": worker.cnh,
                "cnh_category": worker.cnh_category,
                "cnh_emition_date": worker.cnh_emition_date,
                "cnh_valid_date": worker.cnh_valid_date,
                "first_job": worker.first_job,
                "was_employee": worker.was_employee,
                "union_contribute_current_year": worker.union_contribute_current_year,
                "receiving_unemployment_insurance": worker.receiving_unemployment_insurance,
                "previous_experience": worker.previous_experience,
                "month_wage": worker.month_wage,
                "hour_wage": worker.hour_wage,
                "journey_wage": worker.journey_wage,
                "transport_voucher": worker.transport_voucher,
                "transport_voucher_quantity": worker.transport_voucher_quantity,
                "diary_workjourney": worker.diary_workjourney,
                "week_workjourney": worker.week_workjourney,
                "month_workjourney": worker.month_workjourney,
                "experience_time": worker.experience_time,
                "nocturne_hours": worker.nocturne_hours,
                "dangerousness": worker.dangerousness,
                "unhealthy": worker.unhealthy,
                "wage_payment_method": worker.wage_payment_method,
            }
            for worker in workers
        ]


def handle_get_workers_by_turn_and_subsidiarie(turn_id: int, subsidiarie_id: int):
    with Session(engine) as session:
        statement = select(Workers).where(
            Workers.turn_id == turn_id, Workers.subsidiarie_id == subsidiarie_id
        )

        workers = session.exec(statement).all()

    return workers


def handle_get_active_workers_by_turn_and_subsidiarie(
    turn_id: int, subsidiarie_id: int
):
    with Session(engine) as session:
        statement = (
            select(Workers.id, Workers.name, Workers.function_id, Function.name)
            .join(Function, Function.id == Workers.function_id)
            .where(
                Workers.turn_id == turn_id,
                Workers.subsidiarie_id == subsidiarie_id,
                Workers.is_active == True,
            )
        )

        workers = session.exec(statement).all()

        workers_with_no_today_scales = []

        for worker in workers:
            # Query para buscar escalas do trabalhador
            statement = select(Scale).where(Scale.worker_id == worker.id)
            worker_scales = session.exec(statement).all()

            # Verificando se a data de hoje está nas escalas do trabalhador
            worker_scales_contains_today = any(
                date.today().strftime("%d-%m-%Y") in scale.date
                for scale in worker_scales
            )

            # Se a data de hoje não for encontrada, adiciona o trabalhador à lista
            if not worker_scales_contains_today:
                workers_with_no_today_scales.append(
                    {
                        "worker_id": worker[0],
                        "worker_name": worker[1],
                        "function_id": worker[2],
                        "function_name": worker[3],
                    }
                )

        return workers_with_no_today_scales


def handle_get_active_workers_by_subsidiarie_and_function(
    subsidiarie_id: int, function_id: int
):
    with Session(engine) as session:
        active_workers = session.exec(
            select(Workers).where(
                Workers.subsidiarie_id == subsidiarie_id,
                Workers.function_id == function_id,
                Workers.is_active == True,
            )
        ).all()

        return active_workers


def handle_get_workers_by_subsidiaries_functions_and_turns(
    subsidiarie_id: int, function_id: int, turn_id: int
):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.function_id == function_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        return workers


def handle_get_worker_notations(id: int):
    with Session(engine) as session:
        worker_notations = session.exec(
            select(WorkersNotations).where(WorkersNotations.worker_id == id)
        ).all()

        return worker_notations


def handle_post_worker(worker: Workers):
    with Session(engine) as session:
        session.add(worker)

        session.commit()

        session.refresh(worker)

        return worker


def handle_post_worker_notation(id: int, data: PostWorkerNotationInput):
    with Session(engine) as session:
        worker_notation = WorkersNotations(notation=data.notation, worker_id=id)

        session.add(worker_notation)

        session.commit()

        session.refresh(worker_notation)

        return worker_notation


def handle_put_worker(id: int, worker: Workers):
    with Session(engine) as session:
        db_worker = session.get(Workers, id)

        db_worker.name = worker.name if worker.name else db_worker.name

        db_worker.function_id = (
            worker.function_id if worker.function_id else db_worker.function_id
        )

        db_worker.subsidiarie_id = (
            worker.subsidiarie_id if worker.subsidiarie_id else db_worker.subsidiarie_id
        )

        db_worker.is_active = (
            worker.is_active if worker.is_active is not None else db_worker.is_active
        )

        db_worker.turn_id = worker.turn_id if worker.turn_id else db_worker.turn_id

        db_worker.cost_center_id = (
            worker.cost_center_id if worker.cost_center_id else db_worker.cost_center_id
        )

        db_worker.department_id = (
            worker.department_id if worker.department_id else db_worker.department_id
        )

        db_worker.admission_date = (
            worker.admission_date if worker.admission_date else db_worker.admission_date
        )

        db_worker.first_review_date = (
            datetime.strptime(db_worker.admission_date, "%Y-%m-%d") + timedelta(days=30)
        ).strftime("%Y-%m-%d")

        db_worker.second_review_date = (
            datetime.strptime(db_worker.admission_date, "%Y-%m-%d") + timedelta(days=60)
        ).strftime("%Y-%m-%d")

        db_worker.resignation_date = (
            worker.resignation_date
            if worker.resignation_date
            else db_worker.resignation_date
        )

        db_worker.enrolment = (
            worker.enrolment if worker.enrolment else db_worker.enrolment
        )

        db_worker.sales_code = (
            worker.sales_code if worker.sales_code else db_worker.sales_code
        )

        db_worker.picture = worker.picture if worker.picture else db_worker.picture

        db_worker.timecode = worker.timecode if worker.timecode else db_worker.timecode

        db_worker.esocial = worker.esocial if worker.esocial else db_worker.esocial

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

    return db_worker


def handle_reactivate_worker(id: int):
    with Session(engine) as session:
        worker = session.get(Workers, id)

        worker.is_active = True

        session.add(worker)

        session.commit()

        session.refresh(worker)

        return worker


def handle_deactivate_worker(id: int, worker: WorkerDeactivateInput):
    with Session(engine) as session:
        db_worker = session.get(Workers, id)

        db_worker.is_active = (
            worker.is_active if worker.is_active is not None else db_worker.is_active
        )

        db_worker.resignation_reason_id = (
            worker.resignation_reason
            if worker.resignation_reason
            else db_worker.resignation_reason_id
        )

        db_worker.resignation_date = (
            worker.resignation_date
            if worker.resignation_date
            else db_worker.resignation_date
        )

        session.commit()

        session.refresh(db_worker)
    return db_worker


def handle_delete_worker_notation(id: int):
    with Session(engine) as session:
        worker_notation = session.get(WorkersNotations, id)

        session.delete(worker_notation)

        session.commit()

        return {"status": "ok"}
