from app import db
from app.models import Nota, Usuario
from flask import Blueprint, jsonify, request

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notas", methods=["POST"])
def crear_nota():
    try:
        data = request.get_json(silent=True)

        # Validar que los datos existen y son correctos antes de procesarlos
        if (
            not data
            or "email" not in data
            or "titulo" not in data
            or "contenido" not in data
        ):
            return (
                jsonify(
                    {"error": "Faltan datos requeridos: email, título y contenido"}
                ),
                400,
            )

        # Convertir el título a string si el usuario envía un número
        if "titulo" in data:
            data["titulo"] = str(data["titulo"])

        usuario = Usuario.query.filter_by(email=data["email"]).first()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        nueva_nota = Nota(
            usuario_id=usuario.id, titulo=data["titulo"], contenido=data["contenido"]
        )
        db.session.add(nueva_nota)
        db.session.commit()
        return jsonify({"mensaje": "Nota creada correctamente"}), 201

    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@notes_bp.route("/usuarios/<int:usuario_id>/notas", methods=["GET"])
def obtener_notas(usuario_id):
    notas = Nota.query.filter_by(usuario_id=usuario_id).all()
    resultado = [
        {
            "id": n.id,
            "titulo": n.titulo,
            "contenido": n.contenido,
            "fecha": n.fecha_creacion,
        }
        for n in notas
    ]
    return jsonify(resultado), 200


@notes_bp.route("/notas/<int:nota_id>", methods=["GET", "PUT", "DELETE"])
def manejar_nota(nota_id):
    nota = Nota.query.get(nota_id)

    if not nota:
        return jsonify({"error": "Nota no encontrada"}), 404

    if request.method == "GET":
        return (
            jsonify(
                {
                    "id": nota.id,
                    "titulo": nota.titulo,
                    "contenido": nota.contenido,
                    "fecha": nota.fecha_creacion,
                }
            ),
            200,
        )

    elif request.method == "PUT":
        data = request.get_json(silent=True)

        if not data or "titulo" not in data or "contenido" not in data:
            return (
                jsonify({"error": "Faltan datos requeridos: título y contenido"}),
                400,
            )

        nota.titulo = data["titulo"]
        nota.contenido = data["contenido"]
        db.session.commit()
        return jsonify({"mensaje": "Nota actualizada correctamente"}), 200

    elif request.method == "DELETE":
        db.session.delete(nota)
        db.session.commit()
        return jsonify({"mensaje": "Nota eliminada correctamente"}), 200
