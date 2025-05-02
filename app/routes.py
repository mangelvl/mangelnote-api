from app import app, db
from flask import request, jsonify, render_template
from app.models import Usuario, Nota
from sqlalchemy import text  

# Ruta de inicio - Muestra el estado del servidor y la base de datos en una página HTML
@app.route('/')
def home():
    try:
        db.session.execute(text("SELECT 1"))  
        mensaje_db = "Conexión a la base de datos exitosa"
    except Exception as e:
        mensaje_db = f"Error de conexión: {str(e)}"

    return render_template('home.html', mensaje="Flask Server On", estado_base_datos=mensaje_db)

# Manejo de usuarios (GET y POST)
@app.route('/usuarios', methods=['GET', 'POST'])
def manejar_usuarios():
    if request.method == 'GET':
        usuarios = Usuario.query.all()
        resultado = [{"id": u.id, "nombre": u.nombre, "email": u.email} for u in usuarios]
        return jsonify(resultado), 200

    elif request.method == 'POST':
        data = request.json
        nuevo_usuario = Usuario(nombre=data["nombre"], email=data["email"], contraseña=data["contraseña"])

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje": "Usuario creado correctamente"}), 201

# Obtener un usuario por ID
@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if usuario:
        return jsonify({"id": usuario.id, "nombre": usuario.nombre, "email": usuario.email}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Actualizar un usuario por ID
@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    data = request.json
    usuario = Usuario.query.get(usuario_id)

    if usuario:
        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.email = data.get("email", usuario.email)
        usuario.contraseña = data.get("contraseña", usuario.contraseña)

        db.session.commit()
        return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Eliminar un usuario por ID
@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if usuario:
        # Eliminar todas las notas del usuario antes de eliminarlo
        Nota.query.filter_by(usuario_id=usuario.id).delete()
        
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({"mensaje": "Usuario y sus notas eliminados correctamente"}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Crear una nueva nota asociada a un usuario
@app.route('/notas', methods=['POST'])
def crear_nota():
    data = request.json
    usuario = Usuario.query.filter_by(email=data["email"]).first()

    if usuario:
        nueva_nota = Nota(usuario_id=usuario.id, titulo=data["titulo"], contenido=data["contenido"])
        db.session.add(nueva_nota)
        db.session.commit()
        return jsonify({"mensaje": "Nota creada correctamente"}), 201
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Obtener todas las notas de un usuario por ID
@app.route('/usuarios/<int:usuario_id>/notas', methods=['GET'])
def obtener_notas(usuario_id):
    notas = Nota.query.filter_by(usuario_id=usuario_id).all()
    resultado = [{"id": nota.id, "titulo": nota.titulo, "contenido": nota.contenido, "fecha": nota.fecha_creacion} for nota in notas]
    return jsonify(resultado), 200

# Obtener una nota específica por ID
@app.route('/notas/<int:nota_id>', methods=['GET'])
def obtener_nota(nota_id):
    nota = Nota.query.get(nota_id)

    if nota:
        return jsonify({"id": nota.id, "titulo": nota.titulo, "contenido": nota.contenido, "fecha": nota.fecha_creacion}), 200
    else:
        return jsonify({"error": "Nota no encontrada"}), 404

# Actualizar una nota por ID
@app.route('/notas/<int:nota_id>', methods=['PUT'])
def actualizar_nota(nota_id):
    data = request.json
    nota = Nota.query.get(nota_id)

    if nota:
        nota.titulo = data.get("titulo", nota.titulo)
        nota.contenido = data.get("contenido", nota.contenido)

        db.session.commit()
        return jsonify({"mensaje": "Nota actualizada correctamente"}), 200
    else:
        return jsonify({"error": "Nota no encontrada"}), 404

# Eliminar una nota por ID
@app.route('/notas/<int:nota_id>', methods=['DELETE'])
def eliminar_nota(nota_id):
    nota = Nota.query.get(nota_id)

    if nota:
        db.session.delete(nota)
        db.session.commit()
        return jsonify({"mensaje": "Nota eliminada correctamente"}), 200
    else:
        return jsonify({"error": "Nota no encontrada"}), 404
    