from routes.auth_routes import auth_routes
from routes.root_routes import root_routes
from routes.scripts_routes import scripts_routes

public_routes = [
    root_routes,
    auth_routes,
    scripts_routes,
]
