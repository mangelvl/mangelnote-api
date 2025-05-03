from app import db
from app.models import Nota, Usuario
from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__)


@users_bp.route("/usuarios", methods=["GET", "POST"])
def manejar_usuarios():
    if request.method == "GET":
        usuarios = Usuario.query.all()
        return (
            jsonify(
                [{"id": u.id, "nombre": u.nombre, "email": u.email} for u in usuarios]
            ),
            200,
        )

    elif request.method == "POST":
        data = request.get_json(silent=True)

        # Validar que los datos existen y son correctos antes de procesarlos
        if (
            not data
            or "nombre" not in data
            or "email" not in data
            or "contraseña" not in data
        ):
            return (
                jsonify(
                    {"error": "Faltan datos requeridos: nombre, email y contraseña"}
                ),
                400,
            )

        nuevo_usuario = Usuario(
            nombre=data["nombre"], email=data["email"], contraseña=data["contraseña"]
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado correctamente"}), 201


@users_bp.route("/usuarios/<int:usuario_id>", methods=["GET", "PUT", "DELETE"])
def manejar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if request.method == "GET":
        return (
            jsonify(
                {"id": usuario.id, "nombre": usuario.nombre, "email": usuario.email}
            ),
            200,
        )

    elif request.method == "PUT":
        data = request.json
        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.email = data.get("email", usuario.email)
        usuario.contraseña = data.get("contraseña", usuario.contraseña)
        db.session.commit()
        return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200

    elif request.method == "DELETE":
        Nota.query.filter_by(
            usuario_id=usuario.id
        ).delete()  # Eliminar notas del usuario
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario y sus notas eliminados correctamente"}), 200
