from routes.applicants_routes import routes as applicants_routes
from routes.away_reasons_routes import away_reasons_routes
from routes.banks_routes import banks_routes
from routes.cities_routes import cities_routes
from routes.civil_status_routes import civil_status_routes
from routes.cost_center_routes import cost_center_routes
from routes.custom_notifications_routes import custom_notifications_routes
from routes.dates_events_routes import dates_events_routes
from routes.department_routes import department_routes
from routes.discount_reasons_routes import discount_reasons_routes
from routes.ethnicities_routes import ethnicities_routes
from routes.functions_routes import functions_routes
from routes.genders_routes import genders_routes
from routes.hollidays_schedule_routes import hollidays_schedule_routes
from routes.indicators_criteria_routes import indicators_criteria_routes
from routes.indicators_routes import indicators_routes
from routes.nationalities_routes import nationalities_routes
from routes.neighborhoods_routes import neighborhoods_routes
from routes.open_positions_routes import routes as open_positions_routes
from routes.parents_type_routes import parents_type_routes
from routes.resignable_reasons_routes import resignable_reasons_routes
from routes.roles_routes import roles_routes
from routes.scales_routes import scales_routes
from routes.school_levels_routes import school_levels_routes
from routes.states_routes import states_routes
from routes.subsidiaries_routes import subsidiaries_routes
from routes.system_log_routes import system_log_routes
from routes.turns_routes import turns_routes
from routes.users_routes import users_routes
from routes.workers_discounts_routes import workers_discounts_routes
from routes.workers_routes import workers_routes

private_routes = [
    system_log_routes,
    users_routes,
    subsidiaries_routes,
    turns_routes,
    functions_routes,
    roles_routes,
    scales_routes,
    cost_center_routes,
    department_routes,
    resignable_reasons_routes,
    dates_events_routes,
    genders_routes,
    civil_status_routes,
    ethnicities_routes,
    away_reasons_routes,
    school_levels_routes,
    banks_routes,
    parents_type_routes,


    hollidays_schedule_routes,
    workers_routes,
    open_positions_routes,
    applicants_routes,
    nationalities_routes,
    states_routes,
    cities_routes,
    neighborhoods_routes,
    indicators_criteria_routes,
    indicators_routes,
    custom_notifications_routes,
    discount_reasons_routes,
    workers_discounts_routes,
]