from app.config import DATABASE_URI
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Iniciar Flask
app = Flask(__name__)

# Configurar SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar SQLAlchemy para la base de datos
db = SQLAlchemy(app)

# Importar rutas después de inicializar app y db para evitar importaciones circulares
from app import routes  # noqa: E402, F401
