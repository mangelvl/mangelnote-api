from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Importar la configuracion de la base de datos
from app.config import DATABASE_URI

# Iniciar Flask
app = Flask(__name__)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniciar SQLAlchemy para la base de datos
db = SQLAlchemy(app)

# Importar rutas después de iniciar db
from app import routes
