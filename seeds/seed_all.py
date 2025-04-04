from seeds.demission_reasons import demission_reasons
from seeds.seed_away_reasons import seed_away_reasons
from seeds.seed_banks import seed_banks
from seeds.seed_candidate_status import seed_candidate_status
from seeds.seed_cities import seed_cities
from seeds.seed_civil_status import seed_civil_status
from seeds.seed_countries import seed_countries
from seeds.seed_ethnicity import seed_ethnicities
from seeds.seed_genders import seed_genders
from seeds.seed_months import seed_months
from seeds.seed_neighborhoods import seed_neighborhoods
from seeds.seed_roles import seed_roles
from seeds.seed_school_levels import seed_school_levels
from seeds.seed_states import seed_states
from seeds.seed_subsidiaries import seed_subsidiaries
from seeds.seed_users import seed_users


def seed_database():
    demission_reasons()
    seed_roles()
    seed_users()
    seed_subsidiaries()
    seed_candidate_status()
    seed_months()
    seed_civil_status()
    seed_genders()
    seed_states()
    seed_cities()
    seed_neighborhoods()
    seed_ethnicities()
    # seed_countries()
    seed_away_reasons()
    seed_school_levels()
    seed_banks()
