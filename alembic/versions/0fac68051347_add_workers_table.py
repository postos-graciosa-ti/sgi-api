"""add workers table

Revision ID: 0fac68051347
Revises:
Create Date: 2025-03-31 15:35:56.614070

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import inspect

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0fac68051347"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table_name, column_name):
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = inspector.get_columns(table_name)
    return any(column["name"] == column_name for column in columns)


def table_exists(table_name):
    bind = op.get_bind()
    inspector = inspect(bind)
    return inspector.has_table(table_name)


def upgrade() -> None:
    """Upgrade schema."""
    if not table_exists("workers"):
        op.create_table(
            "workers", sa.Column("id", sa.Integer(), nullable=False, primary_key=True)
        )

    # Lista de colunas com suas definições
    columns_to_add = [
        ("name", sa.String(), False, None, True),
        ("function_id", sa.Integer(), True, "function.id", None),
        ("subsidiarie_id", sa.Integer(), True, "subsidiarie.id", None),
        ("is_active", sa.Boolean(), False, None, None, "true"),
        ("turn_id", sa.Integer(), True, "turn.id", None),
        ("cost_center_id", sa.Integer(), True, "costcenter.id", None),
        ("department_id", sa.Integer(), True, "department.id", None),
        ("admission_date", sa.String(), False, None, True),
        ("resignation_date", sa.String(), False, None, True),
        ("resignation_reason_id", sa.Integer(), True, "resignablereasons.id", None),
        ("sales_code", sa.String(), True, None, None),
        ("enrolment", sa.String(), True, None, None),
        ("picture", sa.String(), True, None, None),
        ("timecode", sa.String(), True, None, None),
        ("first_review_date", sa.String(), True, None, None),
        ("second_review_date", sa.String(), True, None, None),
        ("esocial", sa.String(), True, None, None),
        ("teste", sa.String(), True, None, None),
        ("gender_id", sa.Integer(), True, "genders.id", None),
        ("civil_status_id", sa.Integer(), True, "civilstatus.id", None),
        ("street", sa.String(), True, None, None),
        ("street_number", sa.String(), True, None, None),
        ("street_complement", sa.String(), True, None, None),
        ("neighborhood_id", sa.Integer(), True, "neighborhoods.id", None),
        ("cep", sa.String(), True, None, None),
        ("city", sa.Integer(), True, "cities.id", None),
        ("state", sa.Integer(), True, "states.id", None),
        ("phone", sa.String(), True, None, None),
        ("mobile", sa.String(), True, None, None),
        ("email", sa.String(), True, None, None),
        ("ethnicity_id", sa.Integer(), True, "ethnicity.id", None),
        ("birthdate", sa.String(), True, None, None),
        ("birthcity", sa.Integer(), True, "cities.id", None),
        ("birthstate", sa.Integer(), True, "states.id", None),
        ("nationality", sa.String(), True, None, None),
        ("fathername", sa.String(), True, None, None),
        ("mothername", sa.String(), True, None, None),
        ("has_children", sa.Boolean(), True, None, None),
        ("children_data", sa.String(), True, None, None, "[]"),
        ("cpf", sa.String(), True, None, None),
        ("rg", sa.String(), True, None, None),
        ("rg_issuing_agency", sa.String(), True, None, None),
        ("rg_state", sa.Integer(), True, "states.id", None),
        ("rg_expedition_date", sa.String(), True, None, None),
        ("military_cert_number", sa.String(), True, None, None),
        ("pis", sa.String(), True, None, None),
        ("pis_register_date", sa.String(), True, None, None),
        ("votant_title", sa.String(), True, None, None),
        ("votant_zone", sa.String(), True, None, None),
        ("votant_session", sa.String(), True, None, None),
        ("ctps", sa.String(), True, None, None),
        ("ctps_serie", sa.String(), True, None, None),
        ("ctps_state", sa.Integer(), True, "states.id", None),
        ("ctps_emission_date", sa.String(), True, None, None),
        ("cnh", sa.String(), True, None, None),
        ("cnh_category", sa.String(), True, None, None),
        ("cnh_emition_date", sa.String(), True, None, None),
        ("cnh_valid_date", sa.String(), True, None, None),
        ("first_job", sa.Boolean(), True, None, None),
        ("was_employee", sa.Boolean(), True, None, None),
        ("union_contribute_current_year", sa.Boolean(), True, None, None),
        ("receiving_unemployment_insurance", sa.Boolean(), True, None, None),
        ("previous_experience", sa.Boolean(), True, None, None),
        ("month_wage", sa.String(), True, None, None),
        ("hour_wage", sa.String(), True, None, None),
        ("journey_wage", sa.String(), True, None, None),
        ("transport_voucher", sa.String(), True, None, None),
        ("transport_voucher_quantity", sa.String(), True, None, None),
        ("diary_workjourney", sa.String(), True, None, None),
        ("week_workjourney", sa.String(), True, None, None),
        ("month_workjourney", sa.String(), True, None, None),
        ("experience_time", sa.String(), True, None, None),
        ("nocturne_hours", sa.String(), True, None, None),
        ("dangerousness", sa.Boolean(), True, None, None),
        ("unhealthy", sa.Boolean(), True, None, None),
        ("wage_payment_method", sa.String(), True, None, None),
    ]

    for column in columns_to_add:
        col_name = column[0]
        col_type = column[1]
        nullable = column[2]
        fk = column[3]
        index = column[4] if len(column) > 4 else None
        server_default = column[5] if len(column) > 5 else None

        if not column_exists("workers", col_name):
            col_args = [col_name, col_type]
            kwargs = {"nullable": nullable}

            if fk:
                kwargs["sa.ForeignKey"] = fk
            if server_default:
                kwargs["server_default"] = server_default

            op.add_column("workers", sa.Column(*col_args, **kwargs))

            if index:
                op.create_index(f"ix_workers_{col_name}", "workers", [col_name])


def downgrade() -> None:
    """Downgrade schema."""
    # Não removemos colunas no downgrade para evitar perda de dados
    pass
