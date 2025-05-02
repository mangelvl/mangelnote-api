from app import db

# Modelo para los usuarios
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único del usuario
    nombre = db.Column(db.String(80), nullable=False)  # Nombre del usuario
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único
    contraseña = db.Column(db.String(200), nullable=False)  # Contraseña encriptada
    notas = db.relationship("Nota", backref="usuario", lazy=True)  # Relación con notas

# Modelo para las notas
class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único de la nota
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Usuario dueño de la nota
    titulo = db.Column(db.String(100), nullable=False)  # Título de la nota
    contenido = db.Column(db.Text, nullable=False)  # Contenido de la nota
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())  # Fecha de creación
    