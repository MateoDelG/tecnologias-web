from flask import Blueprint, request, jsonify
from db import *
"""Blueprint: Permite modularizar las rutas en Flask, separando routes.py del archivo principal (server.py).
request: Se usa para acceder a los datos de las solicitudes HTTP (GET, POST, PUT, DELETE).
jsonify: Convierte los datos a formato JSON para enviar respuestas HTTP.
Importamos funciones de db.py: obtener_sensores, agregar_sensor, etc., que ejecutan las operaciones CRUD en MongoDB."""

routes = Blueprint("routes", __name__)
"""Blueprint permite definir rutas en un archivo separado (routes.py) y luego registrarlas en server.py."""

@routes.route("/sensores", methods=["GET"])
def route_obtener_sensores():
    """Ruta: /sensores
    Método HTTP: GET
    Acción: Llama a obtener_sensores() en db.py para obtener todos los sensores y devuelve la respuesta en JSON."""
    return jsonify(obtener_sensores())

@routes.route("/sensores/<tipo>", methods=["GET"])
def route_obtener_sensores_por_tipo(tipo):
    """Ruta: /sensores/<tipo> (Ejemplo: /sensores/temperatura)
    Método HTTP: GET
    Acción:
        Llama a obtener_sensores_por_tipo(tipo).
        Si el tipo no es válido, devuelve un error 400 (Bad Request).
        Si es válido, devuelve la lista de sensores de ese tipo."""
    sensores_tipo = obtener_sensores_por_tipo(tipo)
    if sensores_tipo is None:
        return jsonify({"error": "Tipo de sensor inválido"}), 400
    return jsonify(sensores_tipo)

@routes.route("/sensores", methods=["POST"])
def route_agregar_sensor():
    """Ruta: /sensores
    Método HTTP: POST
    Acción:
        Recibe un sensor en formato JSON.
        Llama a agregar_sensor(sensor), que valida los datos y lo guarda en MongoDB.
        Si `sensor_id` ya existe, devuelve un error 409 (Conflict).
        Si los datos son incorrectos, devuelve un error 400.
        Si se guarda correctamente, responde con 201 Created."""
    
    sensor = request.json

    # Validar que se envió sensor_id
    if "sensor_id" not in sensor or not sensor["sensor_id"]:
        return jsonify({"error": "sensor_id es obligatorio"}), 400

    # Intentar agregar el sensor
    resultado = agregar_sensor(sensor)

    # Manejar errores de validación
    if resultado == "EXISTE":
        return jsonify({"error": "El sensor_id ya existe"}), 409  # Código 409 = Conflicto (duplicado)
    
    if resultado is None:
        return jsonify({"error": "Datos inválidos"}), 400

    return jsonify(resultado), 201  # Código 201 = Creado


@routes.route("/sensores/<sensor_id>", methods=["PUT"])
def route_actualizar_sensor(sensor_id):
    """Ruta: /sensores/<sensor_id> (Ejemplo: /sensores/sensor_123)
    Método HTTP: PUT
    Acción:
        Recibe los datos actualizados en JSON.
        Llama a actualizar_sensor(sensor_id, datos_actualizados).
        Si no encuentra un sensor con ese ID, devuelve un error 404.
        Si lo encuentra, lo actualiza y responde con 200 OK."""
    
    datos_actualizados = request.json
    if actualizar_sensor(sensor_id, datos_actualizados):
        return jsonify({"mensaje": "Sensor actualizado"}), 200
    return jsonify({"error": "No se encontró un sensor con ese sensor_id"}), 404


@routes.route("/sensores/<sensor_id>", methods=["DELETE"])
def route_eliminar_sensor(sensor_id):
    """Ruta: /sensores/<sensor_id> (Ejemplo: /sensores/sensor_123)
    Método HTTP: DELETE
    Acción:
        Llama a eliminar_sensor(sensor_id).
        Si no encuentra un sensor con ese ID, devuelve 404.
        Si lo encuentra y elimina, responde con 200 OK."""
    
    if eliminar_sensor(sensor_id):
        return jsonify({"mensaje": "Sensor eliminado"}), 200
    return jsonify({"error": "No se encontró un sensor con ese sensor_id"}), 404

@routes.route("/sensores", methods=["DELETE"])
def route_eliminar_todos_los_sensores():
    """Ruta: /sensores
    Método HTTP: DELETE
    Acción:
        Llama a eliminar_todos_los_sensores().
        Si se eliminan sensores, responde con 200 OK.
        Si no había sensores, responde con 204 No Content."""
    
    if eliminar_todos_los_sensores():
        return jsonify({"mensaje": "Todos los sensores han sido eliminados"}), 200
    
    return jsonify({"mensaje": "No había sensores para eliminar"}), 204