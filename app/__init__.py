from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

    db.init_app(app)
    migrate.init_app(app, db)

    # Registro de blueprints pode ser feito aqui, ou no main.py
    from app.controllers.ClienteController import cliente_bp
    from app.controllers.SeletorController import seletor_bp
    from app.controllers.TransacaoController import transacao_bp
    from app.controllers.ValidadorController import validador_bp
    from app.controllers.SeletorLocalController import seletorlocal_bp


    app.register_blueprint(cliente_bp)
    app.register_blueprint(seletor_bp)
    app.register_blueprint(transacao_bp)
    app.register_blueprint(validador_bp)
    app.register_blueprint(seletorlocal_bp)


    return app
