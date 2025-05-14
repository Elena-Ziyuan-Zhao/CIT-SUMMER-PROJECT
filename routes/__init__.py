
from .admin_routes import admin_bp
from .auth import auth

def register_routes(app):
    app.register_blueprint(admin_bp)

