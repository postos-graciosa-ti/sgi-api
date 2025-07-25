import json
import os
import smtplib
import tempfile
import threading
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from functools import wraps
from io import BytesIO
from typing import Annotated, Any, Callable, Dict, List, Optional, Set

from cachetools import TTLCache, cached
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from openpyxl import Workbook
from pydantic import BaseModel
from sqlalchemy import and_, create_engine, event, inspect, text
from sqlmodel import Session, select, update

from database.sqlite import engine
from functions.logs import log_action
from models.away_reasons import AwayReasons
from models.banks import Banks
from models.cities import Cities
from models.civil_status import CivilStatus
from models.cnh_categories import CnhCategories
from models.cost_center import CostCenter
from models.department import Department
from models.ethnicity import Ethnicity
from models.function import Function
from models.genders import Genders
from models.hierarchy_structure import HierarchyStructure
from models.jobs import Jobs
from models.nationalities import Nationalities
from models.neighborhoods import Neighborhoods
from models.resignable_reasons import ResignableReasons
from models.scale import Scale
from models.school_levels import SchoolLevels
from models.states import States
from models.subsidiarie import Subsidiarie
from models.turn import Turn
from models.user import User
from models.wage_payment_method import WagePaymentMethod
from models.workers import (
    GetWorkersVtReportBody,
    MetricsUpdateRequest,
    PatchWorkersTurnBody,
    Workers,
    WorkersAway,
)
from models.workers_metrics import WorkersMetrics
from models.workers_notations import WorkersNotations
from pyhints.scales import WorkerDeactivateInput
from pyhints.workers import PostWorkerNotationInput
from repositories.patch_record import patch_record

# cache = TTLCache(maxsize=100, ttl=600)

# _cache_invalidation_map = {}


# def register_cache_invalidation(model: Any, cache_func: Callable):
#     if model not in _cache_invalidation_map:
#         _cache_invalidation_map[model] = []

#         _setup_model_listeners(model)

#     _cache_invalidation_map[model].append(cache_func)


# def _setup_model_listeners(model: Any):
#     @event.listens_for(model, "after_insert")
#     @event.listens_for(model, "after_update")
#     @event.listens_for(model, "after_delete")
#     def receive_after_change(mapper, connection, target):
#         if model in _cache_invalidation_map:
#             for cache_func in _cache_invalidation_map[model]:
#                 cache_func.invalidate_cache()


# def cached(cache_store: TTLCache):
#     def decorator(func):
#         def invalidate_cache():
#             cache_store.clear()

#         func.invalidate_cache = invalidate_cache

#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             key = (func.__name__, args, frozenset(kwargs.items()))

#             if key in cache_store:
#                 return cache_store[key]

#             result = func(*args, **kwargs)

#             cache_store[key] = result

#             return result

#         return wrapper

#     return decorator


# MODELS_TO_TRACK = [
#     Workers,
#     Function,
#     Turn,
#     CostCenter,
#     Department,
#     ResignableReasons,
#     Genders,
#     CivilStatus,
#     Neighborhoods,
#     Cities,
#     States,
#     Ethnicity,
#     CnhCategories,
#     WagePaymentMethod,
#     AwayReasons,
#     SchoolLevels,
#     Banks,
#     Nationalities,
#     HierarchyStructure,
# ]


# @cached(cache)
def handle_get_workers_by_subsidiarie(subsidiarie_id: int):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .order_by(Workers.name)
        ).all()

        function_ids = {w.function_id for w in workers if w.function_id}

        turn_ids = {w.turn_id for w in workers if w.turn_id}

        cost_center_ids = {w.cost_center_id for w in workers if w.cost_center_id}

        department_ids = {w.department_id for w in workers if w.department_id}

        resignation_reason_ids = {
            w.resignation_reason_id for w in workers if w.resignation_reason_id
        }

        gender_ids = {w.gender_id for w in workers if w.gender_id}

        civil_status_ids = {w.civil_status_id for w in workers if w.civil_status_id}

        neighborhood_ids = {w.neighborhood_id for w in workers if w.neighborhood_id}

        city_ids = {w.city for w in workers if w.city}

        state_ids = {w.state for w in workers if w.state}

        ethnicity_ids = {w.ethnicity_id for w in workers if w.ethnicity_id}

        birthcity_ids = {w.birthcity for w in workers if w.birthcity}

        birthstate_ids = {w.birthstate for w in workers if w.birthstate}

        rg_state_ids = {w.rg_state for w in workers if w.rg_state}

        ctps_state_ids = {w.ctps_state for w in workers if w.ctps_state}

        cnh_category_ids = {w.cnh_category for w in workers if w.cnh_category}

        wage_payment_method_ids = {
            w.wage_payment_method for w in workers if w.wage_payment_method
        }

        away_reason_ids = {w.away_reason_id for w in workers if w.away_reason_id}

        school_level_ids = {w.school_level for w in workers if w.school_level}

        bank_ids = {w.bank for w in workers if w.bank}

        nationality_ids = {w.nationality for w in workers if w.nationality}

        hierarchy_structure_ids = {
            w.hierarchy_structure for w in workers if w.hierarchy_structure
        }

        functions = (
            session.exec(select(Function).where(Function.id.in_(function_ids))).all()
            if function_ids
            else []
        )

        turns = (
            session.exec(select(Turn).where(Turn.id.in_(turn_ids))).all()
            if turn_ids
            else []
        )

        cost_centers = (
            session.exec(
                select(CostCenter).where(CostCenter.id.in_(cost_center_ids))
            ).all()
            if cost_center_ids
            else []
        )

        departments = (
            session.exec(
                select(Department).where(Department.id.in_(department_ids))
            ).all()
            if department_ids
            else []
        )

        resignation_reasons = (
            session.exec(
                select(ResignableReasons).where(
                    ResignableReasons.id.in_(resignation_reason_ids)
                )
            ).all()
            if resignation_reason_ids
            else []
        )

        genders = (
            session.exec(select(Genders).where(Genders.id.in_(gender_ids))).all()
            if gender_ids
            else []
        )

        civil_statuses = (
            session.exec(
                select(CivilStatus).where(CivilStatus.id.in_(civil_status_ids))
            ).all()
            if civil_status_ids
            else []
        )

        neighborhoods = (
            session.exec(
                select(Neighborhoods).where(Neighborhoods.id.in_(neighborhood_ids))
            ).all()
            if neighborhood_ids
            else []
        )

        cities = (
            session.exec(select(Cities).where(Cities.id.in_(city_ids))).all()
            if city_ids
            else []
        )

        states = (
            session.exec(select(States).where(States.id.in_(state_ids))).all()
            if state_ids
            else []
        )

        ethnicities = (
            session.exec(select(Ethnicity).where(Ethnicity.id.in_(ethnicity_ids))).all()
            if ethnicity_ids
            else []
        )

        birthcities = (
            session.exec(select(Cities).where(Cities.id.in_(birthcity_ids))).all()
            if birthcity_ids
            else []
        )

        birthstates = (
            session.exec(select(States).where(States.id.in_(birthstate_ids))).all()
            if birthstate_ids
            else []
        )

        rg_states = (
            session.exec(select(States).where(States.id.in_(rg_state_ids))).all()
            if rg_state_ids
            else []
        )

        ctps_states = (
            session.exec(select(States).where(States.id.in_(ctps_state_ids))).all()
            if ctps_state_ids
            else []
        )

        cnh_categories = (
            session.exec(
                select(CnhCategories).where(CnhCategories.id.in_(cnh_category_ids))
            ).all()
            if cnh_category_ids
            else []
        )

        wage_payment_methods = (
            session.exec(
                select(WagePaymentMethod).where(
                    WagePaymentMethod.id.in_(wage_payment_method_ids)
                )
            ).all()
            if wage_payment_method_ids
            else []
        )

        away_reasons = (
            session.exec(
                select(AwayReasons).where(AwayReasons.id.in_(away_reason_ids))
            ).all()
            if away_reason_ids
            else []
        )

        school_levels = (
            session.exec(
                select(SchoolLevels).where(SchoolLevels.id.in_(school_level_ids))
            ).all()
            if school_level_ids
            else []
        )

        banks = (
            session.exec(select(Banks).where(Banks.id.in_(bank_ids))).all()
            if bank_ids
            else []
        )

        nationalities = (
            session.exec(
                select(Nationalities).where(Nationalities.id.in_(nationality_ids))
            ).all()
            if nationality_ids
            else []
        )

        hierarchy_structures = (
            session.exec(
                select(HierarchyStructure).where(
                    HierarchyStructure.id.in_(hierarchy_structure_ids)
                )
            ).all()
            if hierarchy_structure_ids
            else []
        )

        functions_dict = {f.id: f for f in functions}

        turns_dict = {t.id: t for t in turns}

        cost_centers_dict = {cc.id: cc for cc in cost_centers}

        departments_dict = {d.id: d for d in departments}

        resignation_reasons_dict = {rr.id: rr for rr in resignation_reasons}

        genders_dict = {g.id: g for g in genders}

        civil_statuses_dict = {cs.id: cs for cs in civil_statuses}

        neighborhoods_dict = {n.id: n for n in neighborhoods}

        cities_dict = {c.id: c for c in cities}

        states_dict = {s.id: s for s in states}

        ethnicities_dict = {e.id: e for e in ethnicities}

        birthcities_dict = {c.id: c for c in birthcities}

        birthstates_dict = {s.id: s for s in birthstates}

        rg_states_dict = {s.id: s for s in rg_states}

        ctps_states_dict = {s.id: s for s in ctps_states}

        cnh_categories_dict = {c.id: c for c in cnh_categories}

        wage_payment_methods_dict = {w.id: w for w in wage_payment_methods}

        away_reasons_dict = {a.id: a for a in away_reasons}

        school_levels_dict = {s.id: s for s in school_levels}

        banks_dict = {b.id: b for b in banks}

        nationalities_dict = {n.id: n for n in nationalities}

        hierarchy_structures_dict = {h.id: h for h in hierarchy_structures}

        result = []

        for worker in workers:
            function = functions_dict.get(worker.function_id)

            turn = turns_dict.get(worker.turn_id)

            cost_center = cost_centers_dict.get(worker.cost_center_id)

            department = departments_dict.get(worker.department_id)

            resignation_reason = resignation_reasons_dict.get(
                worker.resignation_reason_id
            )

            gender = genders_dict.get(worker.gender_id)

            civil_status = civil_statuses_dict.get(worker.civil_status_id)

            neighborhood = neighborhoods_dict.get(worker.neighborhood_id)

            city = cities_dict.get(worker.city)

            state = states_dict.get(worker.state)

            ethnicity = ethnicities_dict.get(worker.ethnicity_id)

            birthcity = birthcities_dict.get(worker.birthcity)

            birthstate = birthstates_dict.get(worker.birthstate)

            rg_state = rg_states_dict.get(worker.rg_state)

            ctps_state = ctps_states_dict.get(worker.ctps_state)

            cnh_category = cnh_categories_dict.get(worker.cnh_category)

            wage_payment_method = wage_payment_methods_dict.get(
                worker.wage_payment_method
            )

            away_reason = away_reasons_dict.get(worker.away_reason_id)

            school_level = school_levels_dict.get(worker.school_level)

            bank = banks_dict.get(worker.bank)

            nationality = nationalities_dict.get(worker.nationality)

            hierarchy_structure = hierarchy_structures_dict.get(
                worker.hierarchy_structure
            )

            result.append(
                {
                    "worker_id": worker.id,
                    "worker_name": worker.name,
                    "worker_is_active": worker.is_active,
                    "admission_date": worker.admission_date,
                    "resignation_date": worker.resignation_date,
                    "resignation_reason_id": worker.resignation_reason_id,
                    "resignation_reason_name": (
                        resignation_reason.name if resignation_reason else None
                    ),
                    "worker_enrolment": worker.enrolment,
                    "worker_sales_code": worker.sales_code,
                    "picture": worker.picture,
                    "timecode": worker.timecode,
                    "first_review_date": worker.first_review_date,
                    "second_review_date": worker.second_review_date,
                    "esocial": worker.esocial,
                    "function_id": worker.function_id,
                    "function_name": function.name if function else None,
                    "turn_id": worker.turn_id,
                    "turn_name": turn.name if turn else None,
                    "turn_start_time": turn.start_time if turn else None,
                    "turn_end_time": turn.end_time if turn else None,
                    "cost_center_id": worker.cost_center_id,
                    "cost_center": cost_center.name if cost_center else None,
                    "department_id": worker.department_id,
                    "department": department.name if department else None,
                    "gender": gender,
                    "civil_status": civil_status,
                    "street": worker.street,
                    "street_number": worker.street_number,
                    "street_complement": worker.street_complement,
                    "neighborhood": neighborhood,
                    "cep": worker.cep,
                    "city": city,
                    "state": state,
                    "phone": worker.phone,
                    "mobile": worker.mobile,
                    "email": worker.email,
                    "ethnicity": ethnicity,
                    "birthdate": worker.birthdate,
                    "birthcity": birthcity,
                    "birthstate": birthstate,
                    "fathername": worker.fathername,
                    "mothername": worker.mothername,
                    "cpf": worker.cpf,
                    "rg": worker.rg,
                    "rg_issuing_agency": worker.rg_issuing_agency,
                    "rg_state": rg_state,
                    "rg_expedition_date": worker.rg_expedition_date,
                    "military_cert_number": worker.military_cert_number,
                    "pis": worker.pis,
                    "pis_register_date": worker.pis_register_date,
                    "votant_title": worker.votant_title,
                    "votant_zone": worker.votant_zone,
                    "votant_session": worker.votant_session,
                    "ctps": worker.ctps,
                    "ctps_serie": worker.ctps_serie,
                    "ctps_state": ctps_state,
                    "ctps_emission_date": worker.ctps_emission_date,
                    "cnh": worker.cnh,
                    "cnh_category": cnh_category,
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
                    "wage_payment_method": wage_payment_method,
                    "is_away": worker.is_away,
                    "away_reason": away_reason,
                    "away_start_date": worker.away_start_date,
                    "away_end_date": worker.away_end_date,
                    "general_function_code": worker.general_function_code,
                    "wage": worker.wage,
                    "last_function_date": worker.last_function_date,
                    "current_function_time": worker.current_function_time,
                    "school_level": school_level,
                    "emergency_number": worker.emergency_number,
                    "bank": bank,
                    "bank_agency": worker.bank_agency,
                    "bank_account": worker.bank_account,
                    "nationality": nationality,
                    "has_children": worker.has_children,
                    "hierarchy_structure": hierarchy_structure,
                    "enterprise_time": worker.enterprise_time,
                    "cbo": worker.cbo,
                    "early_payment": worker.early_payment,
                    "harmfull_exposition": worker.harmfull_exposition,
                    "has_experience_time": worker.has_experience_time,
                    "has_nocturne_hours": worker.has_nocturne_hours,
                    "propotional_payment": worker.propotional_payment,
                    "total_nocturne_workjourney": worker.total_nocturne_workjourney,
                    "twenty_five_workjourney": worker.twenty_five_workjourney,
                    "twenty_two_to_five_week_workjourney": worker.twenty_two_to_five_week_workjourney,
                    "twenty_two_to_five_month_workjourney": worker.twenty_two_to_five_month_workjourney,
                    "twenty_two_to_five_effective_diary_workjourney": worker.twenty_two_to_five_effective_diary_workjourney,
                    "healthcare_plan": worker.healthcare_plan,
                    "healthcare_plan_discount": worker.healthcare_plan_discount,
                    "life_insurance": worker.life_insurance,
                    "life_insurance_discount": worker.life_insurance_discount,
                    "ag": worker.ag,
                    "cc": worker.cc,
                    "early_payment_discount": worker.early_payment_discount,
                    "app_login": worker.app_login,
                }
            )

        return result


# for model in MODELS_TO_TRACK:
#     register_cache_invalidation(model, handle_get_workers_by_subsidiarie)


def handle_get_worker_by_id(id: int):
    with Session(engine) as session:
        worker = session.exec(select(Workers).where(Workers.id == id)).one()

        return worker


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


def handle_get_workers_by_turn_and_function(
    subsidiarie_id: int, turn_id: int, function_id: int
):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.turn_id == turn_id)
            .where(Workers.function_id == function_id)
        ).all()

        return workers


def handle_get_workers_by_turn(subsidiarie_id: int, turn_id: int):
    with Session(engine) as session:
        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        return workers


def handle_get_month_birthdays(id: int) -> List[Dict[str, str]]:
    with Session(engine) as session:
        current_month = date.today().month

        workers = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == id)
            .where(Workers.birthdate != None)
            .where(Workers.is_active == True)
        ).all()

        result = []

        for worker in workers:
            birthdate = worker.birthdate

            if isinstance(birthdate, str):
                try:
                    birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()

                except ValueError:
                    continue

            if birthdate and birthdate.month == current_month:
                result.append({"name": worker.name, "birthdate": birthdate.isoformat()})

        return result


def handle_export_single_worker_excel(worker_id: int):
    label_map = {
        "subsidiarie_id": "Filial",
        "away_reason_id": "Motivo de Afastamento",
        "function_id": "Função",
        "cost_center_id": "Centro de Custo",
        "hierarchy_structure": "Estrutura Hierárquica",
        "department_id": "Departamento",
        "gender_id": "Gênero",
        "ctps_state": "UF CTPS",
        "rg_state": "UF RG",
        "birthcity": "Cidade de Nascimento",
        "birthstate": "Estado de Nascimento",
        "turn_id": "Turno",
        "ethnicity_id": "Etnia",
        "civil_status_id": "Estado Civil",
        "school_level": "Escolaridade",
        "neighborhood_id": "Bairro",
        "city": "Cidade",
        "state": "Estado",
        "bank": "Banco",
        "resignation_reason_id": "Motivo de Demissão",
        "cnh_category": "Categoria CNH",
        "wage_payment_method": "Forma de Pagamento",
        "enrolment": "Matrícula",
        "name": "Nome",
        "is_active": "Ativo",
        "is_away": "Afastado",
        "away_start_date": "Início do Afastamento",
        "away_end_date": "Fim do Afastamento",
        "time_away": "Tempo Afastado",
        "esocial": "E-social",
        "cbo": "CBO",
        "general_function_code": "Código da Função",
        "ctps": "CTPS",
        "ctps_serie": "Série CTPS",
        "ctps_emission_date": "Data de Emissão da CTPS",
        "pis": "PIS",
        "pis_register_date": "Data de Registro do PIS",
        "cpf": "CPF",
        "rg": "RG",
        "rg_issuing_agency": "Órgão Expedidor do RG",
        "rg_expedition_date": "Data de Expedição do RG",
        "fathername": "Nome do Pai",
        "mothername": "Nome da Mãe",
        "birthdate": "Data de Nascimento",
        "nationality": "Nacionalidade",
        "admission_date": "Data de Admissão",
        "enterprise_time": "Tempo de Empresa",
        "wage": "Salário",
        "first_review_date": "1ª Avaliação",
        "second_review_date": "2ª Avaliação",
        "last_function_date": "Data da Última Função",
        "current_function_time": "Tempo na Função Atual",
        "email": "E-mail",
        "street": "Rua",
        "street_number": "Número",
        "street_complement": "Complemento",
        "cep": "CEP",
        "phone": "Telefone",
        "mobile": "Celular",
        "emergency_number": "Telefone de Emergência",
        "bank_agency": "Agência Bancária",
        "bank_account": "Conta Bancária",
        "resignation_date": "Data de Demissão",
        "sales_code": "Código de Vendas",
        "picture": "Foto",
        "timecode": "Código de Ponto",
        "has_children": "Tem Filhos?",
        "children_data": "Dados dos Filhos",
        "military_cert_number": "Número do Certificado Militar",
        "votant_title": "Título de Eleitor",
        "votant_zone": "Zona Eleitoral",
        "votant_session": "Sessão Eleitoral",
        "cnh": "CNH",
        "cnh_emition_date": "Data de Emissão da CNH",
        "cnh_valid_date": "Validade da CNH",
        "first_job": "Primeiro Emprego?",
        "was_employee": "Já foi Funcionário?",
        "union_contribute_current_year": "Contribuição Sindical no Ano",
        "receiving_unemployment_insurance": "Recebendo Seguro-Desemprego",
        "previous_experience": "Experiência Anterior",
        "month_wage": "Salário Mensal",
        "hour_wage": "Salário por Hora",
        "journey_wage": "Salário por Jornada",
        "transport_voucher": "Vale Transporte",
        "transport_voucher_quantity": "Qtd. VT",
        "diary_workjourney": "Jornada Diária",
        "week_workjourney": "Jornada Semanal",
        "month_workjourney": "Jornada Mensal",
        "experience_time": "Tempo de Experiência",
        "nocturne_hours": "Horas Noturnas",
        "dangerousness": "Periculosidade",
        "unhealthy": "Insalubridade",
        "early_payment": "Antecipação Salarial",
        "harmfull_exposition": "Exposição Nociva",
        "has_experience_time": "Tem Tempo de Experiência?",
        "has_nocturne_hours": "Tem Horas Noturnas?",
        "proportional_payment": "Pagamento Proporcional",
        "total_nocturne_workjourney": "Total de Jornada Noturna",
        "twenty_five_workjourney": "Jornada 25%",
        "twenty_two_to_five_week_workjourney": "Jornada 22h-5h Semanal",
        "twenty_two_to_five_month_workjourney": "Jornada 22h-5h Mensal",
        "twenty_two_to_five_effective_diary_workjourney": "22h-5h Efetiva Diária",
        "healthcare_plan": "Plano de Saúde",
        "healthcare_plan_discount": "Desconto do Plano de Saúde",
        "life_insurance": "Seguro de Vida",
        "life_insurance_discount": "Desconto do Seguro de Vida",
        "ag": "Agência",
        "cc": "Conta Corrente",
        "early_payment_discount": "Desconto da Antecipação",
    }

    with Session(engine) as session:
        worker = session.exec(select(Workers).where(Workers.id == worker_id)).first()

        if not worker:
            return {"error": "Colaborador não encontrado"}

    wb = Workbook()

    ws = wb.active

    ws.title = "Colaborador"

    headers = list(label_map.values())

    ws.append(headers)

    row = [getattr(worker, field, "") for field in label_map.keys()]

    ws.append(row)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")

    wb.save(tmp.name)

    tmp.close()

    return FileResponse(
        path=tmp.name,
        filename=f"colaborador_{worker_id}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def handle_get_workers_approaching_two_years(user_id: int):
    with Session(engine) as session:
        user_data = session.get(User, user_id)

        user_subsidiaries = eval(user_data.subsidiaries_id)

        query = select(Workers).where(Workers.subsidiarie_id.in_(user_subsidiaries))

        workers = session.exec(query).all()

        today = datetime.now()

        three_months_later = today + relativedelta(months=3)

        result = []

        for worker in workers:
            try:
                admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d")

                two_year_anniversary = admission_date + relativedelta(years=2)

                if today <= two_year_anniversary <= three_months_later:
                    days_until_anniversary = (two_year_anniversary - today).days

                    worker_data = worker.dict()

                    worker_data["two_year_anniversary_date"] = (
                        two_year_anniversary.strftime("%Y-%m-%d")
                    )

                    worker_data["days_until_anniversary"] = days_until_anniversary

                    result.append(worker_data)

            except Exception as e:
                print(f"Erro ao processar trabalhador {worker.id}: {e}")

        return result


def handle_get_workers_by_functions(
    subsidiarie_id: int, function_id: int, turn_id: int
):
    with Session(engine) as session:
        workers_by_function = session.exec(
            select(
                Workers.enrolment.label("enrolment"),
                Workers.name.label("name"),
                CostCenter.name.label("cost_center"),
                Department.name.label("department"),
            )
            .join(CostCenter, Workers.cost_center_id == CostCenter.id)
            .join(Department, Workers.department_id == Department.id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.is_active == True)  # noqa: E712
            .where(Workers.function_id == function_id)
            .where(Workers.turn_id == turn_id)
        ).all()

        return [
            {
                "enrolment": worker.enrolment,
                "name": worker.name,
                "cost_center": worker.cost_center,
                "department": worker.department,
            }
            for worker in workers_by_function
        ]


def handle_post_worker(request, worker: Workers, user):
    admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d").date()

    first_review = admission_date + relativedelta(months=1)

    second_review = admission_date + relativedelta(months=2)

    worker.first_review_date = first_review.strftime("%Y-%m-%d")

    worker.second_review_date = second_review.strftime("%Y-%m-%d")

    with Session(engine) as session:
        session.add(worker)

        session.commit()

        session.refresh(worker)

        log_action(
            action="post",
            table_name="workers",
            record_id=worker.id,
            user_id=user["id"],
            details={
                "before": None,
                "after": worker.dict(),
            },
            endpoint=str(request.url.path),
        )

        return worker


def handle_post_worker_notation(id: int, data: PostWorkerNotationInput):
    with Session(engine) as session:
        worker_notation = WorkersNotations(notation=data.notation, worker_id=id)

        session.add(worker_notation)

        session.commit()

        session.refresh(worker_notation)

        return worker_notation


def handle_put_worker(request, id: int, worker: Workers, user):
    with Session(engine) as session:
        db_worker = session.get(Workers, id)

        log_action(
            action="put",
            table_name="workers",
            record_id=worker.id,
            user_id=user["id"],
            details={
                "before": db_worker.dict(),
                "after": worker.dict(),
            },
            endpoint=str(request.url.path),
        )

        for field in worker.__fields__.keys():
            value = getattr(worker, field)

            if value is not None:
                setattr(db_worker, field, value)

        if worker.has_nocturne_hours is None:
            db_worker.has_nocturne_hours = None

        if worker.propotional_payment is None:
            db_worker.propotional_payment = None

        if worker.total_nocturne_workjourney is None:
            db_worker.total_nocturne_workjourney = None

        if worker.twenty_five_workjourney is None:
            db_worker.twenty_five_workjourney = None

        if worker.twenty_two_to_five_week_workjourney is None:
            db_worker.twenty_two_to_five_week_workjourney = None

        if worker.twenty_two_to_five_month_workjourney is None:
            db_worker.twenty_two_to_five_month_workjourney = None

        if worker.twenty_two_to_five_effective_diary_workjourney is None:
            db_worker.twenty_two_to_five_effective_diary_workjourney = None

        if worker.admission_date:
            try:
                admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d")

                db_worker.first_review_date = (
                    admission_date + timedelta(days=30)
                ).strftime("%Y-%m-%d")

                db_worker.second_review_date = (
                    admission_date + timedelta(days=60)
                ).strftime("%Y-%m-%d")

            except ValueError:
                pass

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

    return db_worker


def handle_reactivate_worker(request, id: int, user):
    with Session(engine) as session:
        worker = session.get(Workers, id)

        before_state = worker.dict()

        worker.is_active = True

        session.commit()

        session.refresh(worker)

        log_action(
            action="put",
            table_name="workers",
            record_id=worker.id,
            user_id=user["id"],
            details={
                "before": before_state,
                "after": worker.dict(),
            },
            endpoint=str(request.url.path),
        )

        return worker


def handle_worker_away(subsidiarie_id: int, worker_id: int, worker: WorkersAway):
    with Session(engine) as session:
        get_db_worker = (
            select(Workers)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        )

        db_worker = session.exec(get_db_worker).first()

        db_worker.is_away = True

        db_worker.away_start_date = (
            worker.away_start_date
            if worker.away_start_date
            else db_worker.away_start_date
        )

        db_worker.away_end_date = (
            worker.away_end_date if worker.away_end_date else db_worker.away_end_date
        )

        db_worker.away_reason_id = (
            worker.away_reason_id if worker.away_reason_id else db_worker.away_reason_id
        )

        start_date = datetime.strptime(worker.away_start_date, "%Y-%m-%d").date()

        end_date = datetime.strptime(worker.away_end_date, "%Y-%m-%d").date()

        away_days = (end_date - start_date).days + 1

        db_worker.time_away = away_days

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

        return db_worker


def handle_away_return(subsidiarie_id: int, worker_id: int):
    with Session(engine) as session:
        get_db_worker = (
            select(Workers)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        )

        db_worker = session.exec(get_db_worker).first()

        db_worker.is_away = False

        session.add(db_worker)

        session.commit()

        return db_worker


def handle_deactivate_worker(request, id: int, worker: WorkerDeactivateInput, user):
    updates = {
        "is_active": worker.is_active,
        "resignation_reason_id": worker.resignation_reason,
        "resignation_date": worker.resignation_date,
    }

    result = patch_record(
        model=Workers,
        pk_column="id",
        pk_column_value=id,
        updates=updates,
        request=request,
        user=user,
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    try:
        EMAIL_REMETENTE = os.environ["EMAIL_REMETENTE"]

        SENHA = os.environ["SENHA"]

        BCC = os.environ.get("BCC")

        MABECON_EMAIL = os.environ.get("MABECON_EMAIL")

        msg = EmailMessage()

        msg["Subject"] = "Solicitação de demissão de colaborador"

        msg["From"] = EMAIL_REMETENTE

        msg["To"] = MABECON_EMAIL

        msg["Bcc"] = BCC

        msg.set_content(f"Solicitamos o desligamento do colaborador {result.name}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA)

            smtp.send_message(msg)

    except KeyError as e:
        raise HTTPException(
            status_code=500, detail=f"Variável de ambiente ausente: {e}"
        )

    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mail: {str(e)}")

    return {"success": True}


def handle_patch_worker_subsidiarie(worker_id: int, subsidiarie_id: int):
    with Session(engine) as session:
        db_worker = session.exec(select(Workers).where(Workers.id == worker_id)).first()

        db_worker.subsidiarie_id = subsidiarie_id

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

        return {"success": True}


def handle_delete_worker_notation(id: int):
    with Session(engine) as session:
        worker_notation = session.get(WorkersNotations, id)

        session.delete(worker_notation)

        session.commit()

        return {"status": "ok"}


def handle_patch_workers_turn(body: PatchWorkersTurnBody):
    with Session(engine) as session:
        db_worker = session.exec(
            select(Workers).where(Workers.id == body.worker_id)
        ).first()

        db_worker.turn_id = body.turn_id

        db_worker.function_id = body.function_id

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

        return {"success": True}


def handle_get_workers_need_vt(body: GetWorkersVtReportBody):
    with Session(engine) as session:
        start_date = datetime.strptime(body.start_date, "%Y-%m-%d").date()

        end_date = datetime.strptime(body.end_date, "%Y-%m-%d").date()

        workers = session.exec(
            select(Workers).where(Workers.transport_voucher is not None)
        ).all()

        result = []

        for worker in workers:
            admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d").date()

            if admission_date >= start_date and admission_date <= end_date:
                result.append(worker)

        return result


def handle_get_workers_need_open_account(body: GetWorkersVtReportBody):
    with Session(engine) as session:
        start_date = datetime.strptime(body.start_date, "%Y-%m-%d").date()

        end_date = datetime.strptime(body.end_date, "%Y-%m-%d").date()

        workers = session.exec(select(Workers)).all()

        result = []

        for worker in workers:
            admission_date = datetime.strptime(worker.admission_date, "%Y-%m-%d").date()

            if admission_date >= start_date and admission_date <= end_date:
                result.append(worker)

        return result


class RequestBadgesBody(BaseModel):
    workers_ids: List[int]
    recipient_email: str


def handle_post_request_workers_badges(body: RequestBadgesBody):
    EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")

    SENHA = os.environ.get("SENHA")

    workers_ids = body.workers_ids

    with Session(engine) as session:
        wb = Workbook()

        ws = wb.active

        ws.title = "Crachás"

        ws.append(
            ["Função", "Código de Vendas", "Matrícula", "Frente", "Verso", "Filial"]
        )

        for worker_id in workers_ids:
            worker = session.get(Workers, worker_id)

            if not worker:
                continue

            worker_function = session.get(Function, worker.function_id)

            worker_subsidiarie = session.get(Subsidiarie, worker.subsidiarie_id)

            funcao = worker_function.name if worker_function else ""

            codigo_vendas = worker.sales_code or ""

            matricula = worker.esocial or ""

            frente = worker.name.split()[0] if worker.name else ""

            verso = worker.name or ""

            filial = worker_subsidiarie.name if worker_subsidiarie else ""

            ws.append([funcao, codigo_vendas, matricula, frente, verso, filial])

        output = BytesIO()

        wb.save(output)

        output.seek(0)

        try:
            msg = EmailMessage()

            msg["Subject"] = "Planilha de Crachás"

            msg["From"] = EMAIL_REMETENTE

            msg["To"] = body.recipient_email

            msg.set_content("Segue em anexo a planilha de crachás solicitada.")

            msg.add_attachment(
                output.read(),
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename="badges.xlsx",
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA)

                smtp.send_message(msg)

            return JSONResponse(
                content={"detail": "E-mail enviado com sucesso."}, status_code=200
            )

        except Exception as e:
            return JSONResponse(
                content={"detail": f"Erro ao enviar e-mail: {str(e)}"}, status_code=500
            )


def handle_update_worker_metrics(metrics_id: int, body: MetricsUpdateRequest):
    with Session(engine) as session:
        metrics_record = session.get(WorkersMetrics, metrics_id)

        if not metrics_record:
            raise HTTPException(status_code=404, detail="Indicador não encontrado.")

        try:
            existing_metrics = json.loads(metrics_record.metrics or "{}")

            incoming_metrics = json.loads(body.metrics)

            merged = {**existing_metrics, **incoming_metrics}

            metrics_record.metrics = json.dumps(merged)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro no JSON: {str(e)}")

        session.add(metrics_record)

        session.commit()

        session.refresh(metrics_record)

        return {"message": "Indicador atualizado com sucesso.", "data": metrics_record}
