from .admin_routes import admin_bp

def register_routes(app):
    app.register_blueprint(admin_bp)
