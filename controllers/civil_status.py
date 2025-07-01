from models.civil_status import CivilStatus
from repositories.get_all_records import get_all_records


def handle_get_civil_status():
    return get_all_records(CivilStatus)
