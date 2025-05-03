from app import db
from flask import Blueprint, render_template
from sqlalchemy import text

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    try:
        db.session.execute(text("SELECT 1"))
        mensaje_db = "Conexión a la base de datos exitosa"
    except Exception as e:
        mensaje_db = f"Error de conexión: {str(e)}"

    return render_template(
        "home.html", mensaje="Flask Server On", estado_base_datos=mensaje_db
    )
