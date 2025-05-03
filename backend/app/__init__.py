from app.config import DATABASE_URI

# Manejadores globales de errores
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app.routes.main import main_bp  # noqa: E402
from app.routes.notes import notes_bp  # noqa: E402
from app.routes.users import users_bp  # noqa: E402

app.register_blueprint(users_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(main_bp)


# Manejadores globales de errores
@app.errorhandler(404)
def recurso_no_encontrado(error):
    return jsonify({"error": "Recurso no encontrado"}), 404


@app.errorhandler(400)
def solicitud_invalida(error):
    return jsonify({"error": "Solicitud inválida"}), 400


@app.errorhandler(500)
def error_interno(error):
    return jsonify({"error": "Error interno del servidor"}), 500
