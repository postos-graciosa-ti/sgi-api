from migrations.add_attendance_date_to_applicants import (
    add_attendance_date_to_applicants,
)
from migrations.add_coordinator_observations_to_applicants import (
    add_coordinator_observations_to_applicants,
)
from migrations.add_coordinator_opinion_to_applicants import (
    add_coordinator_opinion_to_applicants,
)
from migrations.add_email_to_applicants import add_email_to_applicants
from migrations.add_is_active_to_applicants import add_is_active_to_applicants
from migrations.add_rh_opinion_to_applicants import add_rh_opinion_to_applicants
from migrations.add_school_levels_to_applicants import add_school_levels_to_applicants
from migrations.add_special_notation_to_applicants import (
    add_special_notation_to_applicants,
)


def apply_migrations():
    add_school_levels_to_applicants()

    add_rh_opinion_to_applicants()

    add_coordinator_opinion_to_applicants()

    add_special_notation_to_applicants()

    add_coordinator_observations_to_applicants()

    add_attendance_date_to_applicants()

    add_is_active_to_applicants()

    add_email_to_applicants()
