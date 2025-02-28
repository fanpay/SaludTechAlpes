import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

# Constantes
DB_USER = os.getenv("POSTGRES_USER", default="postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="postgres")
DB_HOST = os.getenv("POSTGRES_HOST", default="localhost")
DB_PORT = os.getenv("POSTGRES_PORT", default="5432")
DB_NAME =  os.getenv("POSTGRES_DB", default="transformacionesdb")

def registrar_handlers():
    import saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion

def importar_modelos_alchemy():
    import saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.dto

def comenzar_consumidor(app):
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.consumidores as anonimizacion

    def suscribirse_a_eventos_con_contexto():
        with app.app_context():
            anonimizacion.suscribirse_a_eventos()

    def suscribirse_a_comandos_con_contexto():
        with app.app_context():
            anonimizacion.suscribirse_a_comandos()
    # Suscripción a eventos
    threading.Thread(target=suscribirse_a_eventos_con_contexto).start()

    # Suscripción a comandos
    threading.Thread(target=suscribirse_a_comandos_con_contexto).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    # Inicializa la DB
    from saludtech.enriquecimiento.config.db import init_db
    init_db(app)

    from saludtech.enriquecimiento.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    # Importa Blueprints
    from . import enriquecimiento

    # Registro de Blueprints
    app.register_blueprint(enriquecimiento.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
