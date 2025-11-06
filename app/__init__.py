from flask import Flask
from .config import Config
from .logger import setup_logging
from .db import db, init_db
from .routes import api_bp

def create_app(testing: bool = False):
    app = Flask(__name__)
    app.config.from_object(Config())
    if testing:
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    setup_logging(app)
    db.init_app(app)
    with app.app_context():
        init_db()
    app.register_blueprint(api_bp, url_prefix="/api")
    @app.get("/health")
    def health():
        return {"status":"ok"}
    return app
