from seeds.demission_reasons import demission_reasons
from seeds.seed_candidate_status import seed_candidate_status
from seeds.seed_months import seed_months
from seeds.seed_roles import seed_roles
from seeds.seed_subsidiaries import seed_subsidiaries
from seeds.seed_users import seed_users


def seed_database():
    demission_reasons()
    seed_roles()
    seed_users()
    seed_subsidiaries()
    seed_candidate_status()
    seed_months()
