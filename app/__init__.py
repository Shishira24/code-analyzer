from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')


    from app.routes.projects import projects_bp
    app.register_blueprint(projects_bp, url_prefix='/projects')

    from app.routes.analysis import analysis_bp
    app.register_blueprint(analysis_bp, url_prefix='/projects')

    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')
    
    with app.app_context():
        db.create_all()

    return app