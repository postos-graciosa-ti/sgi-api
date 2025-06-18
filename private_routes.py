from routes.applicants_routes import routes as applicants_routes
from routes.cities_routes import cities_routes
from routes.functions_routes import functions_routes
from routes.hollidays_schedule_routes import hollidays_schedule_routes
from routes.nationalities_routes import nationalities_routes
from routes.neighborhoods_routes import neighborhoods_routes
from routes.open_positions_routes import routes as open_positions_routes
from routes.roles_routes import roles_routes
from routes.scales_routes import scales_routes
from routes.states_routes import states_routes
from routes.subsidiaries_routes import subsidiaries_routes
from routes.system_log_routes import system_log_routes
from routes.turns_routes import turns_routes
from routes.users_routes import users_routes
from routes.workers_routes import workers_routes

private_routes = [
    system_log_routes,
    users_routes,

    subsidiaries_routes,
    turns_routes,
    functions_routes,
    roles_routes,
    scales_routes,


    hollidays_schedule_routes,

    workers_routes,
    
    open_positions_routes,
    applicants_routes,
    nationalities_routes,
    states_routes,
    cities_routes,
    neighborhoods_routes,
]
