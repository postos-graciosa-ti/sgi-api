import logging
import os
import time
from typing import Set

import psutil
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy_utils import database_exists
from sqlmodel import Session, SQLModel, select

from database.sqlite import create_db_and_tables, engine
from migrations.apply_migrations import apply_migrations
from migrations.lib.watchmen.watch import watch
from models.applicant_process import ApplicantProcess
from models.applicants import Applicants
from models.applicants_docs import ApplicantsDocs
from models.applicants_exams import ApplicantsExams
from models.CustomNotification import CustomNotification
from models.discount_reasons import DiscountReasons
from models.docs_checklist import DocsChecklist
from models.goals import Goals
from models.hollidays_scale import HollidaysScale
from models.indicators import Indicators
from models.indicators_criteria import IndicatorsCriteria
from models.metrics import Metrics
from models.open_positions import OpenPositions
from models.redirected_to import RedirectedTo
from models.system_log import SystemLog
from models.user import User
from models.workers_courses import WorkersCourses
from models.workers_discounts import WorkersDiscounts
from models.workers_metrics import WorkersMetrics
from models.workers_periodic_reviews import WorkersPeriodicReviews
from models.workers_pictures import WorkersPictures
from seeds.seed_all import seed_database

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def handle_watch_models():
    watch(ApplicantsExams)

    watch(Applicants)

    watch(OpenPositions)

    watch(RedirectedTo)

    watch(SystemLog)

    watch(WorkersPeriodicReviews)

    watch(WorkersPictures)

    watch(ApplicantProcess)

    watch(HollidaysScale)

    watch(IndicatorsCriteria)

    watch(Indicators)

    watch(DocsChecklist)

    watch(Goals)

    watch(CustomNotification)

    watch(User)

    watch(Metrics)

    watch(WorkersMetrics)

    watch(DiscountReasons)

    watch(WorkersDiscounts)

    watch(ApplicantsDocs)

    watch(WorkersCourses)


def handle_on_startup():
    try:
        if not database_exists(engine.url):
            print("Banco de dados não encontrado. Criando...")

            create_db_and_tables()

            handle_watch_models()

            apply_migrations()

            seed_database()

        else:
            inspector = inspect(engine)

            tables = inspector.get_table_names()

            if not tables:
                print("Nenhuma tabela encontrada. Criando estrutura inicial...")

                create_db_and_tables()

                handle_watch_models()

                apply_migrations()

                seed_database()

            else:
                print("Banco de dados existente detectado.")

                print("Verificação de banco de dados concluída.")

                handle_watch_models()

                apply_migrations()

                seed_database()

    except OperationalError as e:
        print(f"Erro crítico ao conectar ao banco de dados: {e}")

        raise


def handle_get_docs_info():
    return {"docs": "acess /docs", "redocs": "access /redocs"}


def handle_health_check():
    start_time = time.time()

    db_latency = None

    try:
        logger.info("Iniciando o health check...")

        with Session(engine) as session:
            db_start = time.time()

            inspector = inspect(engine)

            tables = inspector.get_table_names()

            db_latency = round(time.time() - db_start, 4)

            if "user" not in tables:
                logger.warning("Tabela 'user' não encontrada no banco de dados.")

                performance = collect_performance_data(start_time, db_latency)

                logger.info(f"Dados de performance: {performance}")

                return {
                    "success": False,
                    "detail": "Tabela 'user' não encontrada no banco de dados.",
                    "performance": performance,
                }

            logger.info("Tabela 'user' encontrada. Verificando usuários...")

            has_users = session.scalar(select(User)) is not None

            logger.info(f"Usuário encontrado: {has_users}")

            performance = collect_performance_data(start_time, db_latency)

            logger.info(f"Dados de performance: {performance}")

            return {
                "success": True,
                "activated": has_users,
                "performance": performance,
            }

    except SQLAlchemyError as e:
        logger.error(f"Erro no banco de dados: {e}")

        performance = collect_performance_data(start_time, db_latency)

        logger.info(f"Dados de performance: {performance}")

        return {
            "success": False,
            "detail": "Operação no banco de dados falhou.",
            "performance": performance,
        }

    except Exception as e:  # noqa: F841
        logger.exception("Ocorreu um erro inesperado")

        performance = collect_performance_data(start_time, db_latency)

        logger.info(f"Dados de performance: {performance}")

        return {
            "success": False,
            "detail": "Ocorreu um erro inesperado.",
            "performance": performance,
        }


def collect_performance_data(start_time, db_latency=None):
    process = psutil.Process(os.getpid())

    cpu_percent = psutil.cpu_percent(interval=0.1)

    mem_usage_mb = round(process.memory_info().rss / 1024 / 1024, 2)

    latency = round(time.time() - start_time, 4)

    return {
        "latency_seconds": latency,
        "cpu_percent": round(cpu_percent, 2),
        "memory_usage_mb": mem_usage_mb,
        "database_latency_seconds": db_latency,
    }


def get_model_table_names() -> Set[str]:
    return set(SQLModel.metadata.tables.keys())


def get_db_table_names(engine) -> Set[str]:
    inspector = inspect(engine)

    return set(inspector.get_table_names())


def handle_verify_schema_diff():
    database_url = os.environ.get("SQLITE_URL")

    engine = create_engine(database_url)

    inspector = inspect(engine)

    model_tables = get_model_table_names()

    db_tables = get_db_table_names(engine)

    only_in_models = sorted(model_tables - db_tables)

    only_in_db = sorted(db_tables - model_tables)

    in_both = model_tables & db_tables

    column_diffs = []

    for table in sorted(in_both):
        model_columns = set(c.name for c in SQLModel.metadata.tables[table].columns)

        db_columns = set(col["name"] for col in inspector.get_columns(table))

        extra_in_model = sorted(model_columns - db_columns)

        extra_in_db = sorted(db_columns - model_columns)

        if extra_in_model or extra_in_db:
            column_diffs.append(
                {
                    "table": table,
                    "only_in_models": extra_in_model,
                    "only_in_db": extra_in_db,
                }
            )

    return {
        "tables_only_in_models": only_in_models,
        "tables_only_in_db": only_in_db,
        "column_differences": column_diffs,
    }
