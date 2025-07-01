from models.ethnicity import Ethnicity
from repositories.get_all_records import get_all_records


def handle_get_ethnicities():
    return get_all_records(Ethnicity)
