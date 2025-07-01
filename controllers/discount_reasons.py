from models.discount_reasons import DiscountReasons
from repositories.get_all_records import get_all_records


def handle_get_discounts_reasons():
    return get_all_records(DiscountReasons)
