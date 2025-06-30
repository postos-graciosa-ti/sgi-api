from models.genders import Genders
from repositories.get_all_records import get_all_records


def handle_get_genders():
    return get_all_records(Genders)
