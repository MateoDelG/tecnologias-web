
#PASO 1
#Hacer la lectura de este archivo para cargar los datos en una variable.
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Cargar datos desde el archivo JSON
with open("devices.json", "r") as f:
    devices_data = json.load(f)
#FIN PASO 1


#PASO 2
#Verificar que la lectura se hace correctamente imprimiendo los dispositivos en consola al iniciar la app:
# print("Datos iniciales:", devices_data)
#FIN PASO 2


#PASO 3
#Definir un endpoint GET /devices que retorne la lista completa de dispositivos:
@app.route("/devices", methods=["GET"])
def get_devices():
    """
    Esto define una ruta para una aplicación web Flask.
    El decorador @app.route se utiliza para vincular un endpoint URL
    a una función específica. En este caso, el endpoint URL es "/devices"
    y el método HTTP permitido para este endpoint es GET.
    La función get_devices se define para manejar solicitudes al endpoint "/devices".
    Cuando se realiza una solicitud GET a este endpoint, se ejecuta la función.
    La función jsonify convierte devices_data (que se espera que sea una lista
    o un diccionario) en una respuesta con formato JSON. 
    Esta respuesta se devuelve al cliente junto con un código de 
    estado HTTP 200, que indica una solicitud exitosa.
    """
    return jsonify(devices_data), 200
"""
Ejercicio: cree una ruta GET /devices/active que devuelva únicamente
los dispositivos cuyo status sea "active". Esto implica filtrar devices_data antes
de enviarlo en la respuesta.
"""
#FIN PASO 3

#PASO 4
# 1.Definir un endpoint con parámetro en la URL: /devices/<int:device_id>.
# 2.Buscar el dispositivo en devices_data cuyo id coincida con device_id.
# 3.Devolver el objeto en JSON si se encuentra, o un mensaje de error con 404 Not Found si no existe.

@app.route("/devices/<int:device_id>", methods=["GET"])
def get_device(device_id):
    device = None  # Inicialmente, asumimos que el dispositivo no se encuentra
    
    for d in devices_data:  # Recorremos la lista de dispositivos
        if d["id"] == device_id:  # Si encontramos un dispositivo con el ID buscado
            device = d  # Lo guardamos en la variable "device"
            break  # Terminamos la búsqueda
    
    # Si encontramos el dispositivo, lo devolvemos en formato JSON con código 200 (éxito)
    if device:
        return jsonify(device), 200
    else:
        # Si no lo encontramos, devolvemos un mensaje de error con código 404 (no encontrado)
        return jsonify({"error": "Device not found"}), 404
"""
Ejercicio: Solicitar a los estudiantes que añadan una validación extra,
por ejemplo, si el device_id es menor que 1, retornar 400 Bad Request en
lugar de buscarlo en la lista.
"""
#FIN PASO 4

#PASO 5
# 1.Definir la ruta POST /devices.
# 2.Leer el cuerpo (JSON) de la solicitud usando request.json.
# 3.Validar los campos básicos (por ejemplo, que vengan name y type).
# 4.Calcular el id nuevo.
# 5.Agregar el nuevo dispositivo a la lista y guardar en el archivo JSON.


@app.route("/devices", methods=["POST"])
def create_device():
    """
    Crea un nuevo dispositivo a partir de los datos enviados en una solicitud POST.

    Requiere:
    - "name": Nombre del dispositivo (obligatorio).
    - "type": Tipo de dispositivo (obligatorio).
    - "status": Estado del dispositivo (opcional, por defecto "inactive").

    Retorna:
    - JSON con los datos del nuevo dispositivo y código HTTP 201 si se crea correctamente.
    - JSON con un mensaje de error y código HTTP 400 si faltan datos obligatorios.
    """

    # Obtener los datos enviados en la solicitud (esperando que sean JSON)
    data = request.json

    # Validar que los campos "name" y "type" estén presentes en los datos
    if not data.get("name") or not data.get("type"):
        return jsonify({"error": "Missing required fields"}), 400  # Código 400: Bad Request

    # Generar un nuevo ID para el dispositivo:
    # Si la lista 'devices_data' no está vacía, tomamos el ID más alto y sumamos 1.
    # Si la lista está vacía, el primer ID será 1.
    new_id = max(d["id"] for d in devices_data) + 1 if devices_data else 1

    # Crear un nuevo diccionario con los datos del dispositivo
    new_device = {
        "id": new_id,
        "name": data["name"],
        "type": data["type"],
        "status": data.get("status", "inactive")  # Si no se envía "status", se usa "inactive" por defecto
    }

    # Agregar el nuevo dispositivo a la lista en memoria
    devices_data.append(new_device)

    # Guardar la lista actualizada en un archivo JSON para persistencia
    with open("devices.json", "w") as f:
        json.dump(devices_data, f, indent=2)  # 'indent=2' para que el JSON sea más legible

    # Responder con el nuevo dispositivo y código 201 (Created)
    return jsonify(new_device), 201
"""Ejercicio: Pedir que, además de validar name y type, verifiquen que el 
campo type sea uno de los valores permitidos (por ejemplo, "temperature", "pressure", "speed"),
devolviendo 400 Bad Request si no se cumple.
"""
#FIN PASO 5

#PASO 6
# Definir la ruta PUT /devices/<int:device_id>.
# Localizar el dispositivo por device_id.
# Actualizar los campos recibidos.
# Guardar cambios en el archivo JSON.
@app.route("/devices/<int:device_id>", methods=["PUT"])
def update_device(device_id):
    """
    Actualiza los datos de un dispositivo existente.

    Parámetros:
    - device_id: ID del dispositivo que se quiere actualizar (pasado en la URL).

    Datos esperados en el cuerpo de la solicitud (JSON):
    - "name": Nuevo nombre del dispositivo (opcional).
    - "type": Nuevo tipo de dispositivo (opcional).
    - "status": Nuevo estado del dispositivo (opcional).

    Retorna:
    - JSON con los datos actualizados del dispositivo y código HTTP 200 si se actualiza correctamente.
    - JSON con un mensaje de error y código HTTP 404 si el dispositivo no se encuentra.
    """

    # Obtener los datos enviados en la solicitud
    data = request.json

    # Buscar el dispositivo por su ID en la lista
    device = next((d for d in devices_data if d["id"] == device_id), None)

    # Si no se encuentra el dispositivo, devolver un error 404 (Not Found)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    # Actualizar los campos solo si están presentes en la solicitud
    if "name" in data:
        device["name"] = data["name"]
    if "type" in data:
        device["type"] = data["type"]
    if "status" in data:
        device["status"] = data["status"]

    # Guardar la lista actualizada en el archivo JSON para persistencia
    with open("devices.json", "w") as f:
        json.dump(devices_data, f, indent=2)

    # Retornar el dispositivo actualizado con código HTTP 200 (OK)
    return jsonify(device), 200
"""
Ejercicio: Implementar la validación de type durante la actualización (al igual que en el POST),
para que no se pueda cambiar un dispositivo a un tipo no permitido.
"""
#fin PASO 6

#PASO 7
# 1.Definir la ruta DELETE /devices/<int:device_id>.
# 2.Localizar el dispositivo.
# 3.Eliminarlo de la lista y actualizar el archivo JSON.
@app.route("/devices/<int:device_id>", methods=["DELETE"])
def delete_device(device_id):
    """
    Elimina un dispositivo de la lista según su ID.

    Parámetros:
    - device_id: ID del dispositivo que se quiere eliminar (pasado en la URL).

    Retorna:
    - JSON con un mensaje de éxito y código HTTP 200 si el dispositivo fue eliminado.
    - JSON con un mensaje de error y código HTTP 404 si el dispositivo no fue encontrado.
    """

    # Buscar el índice del dispositivo con el ID dado
    index = next((i for i, d in enumerate(devices_data) if d["id"] == device_id), -1)

    # Si el índice es -1, significa que el dispositivo no fue encontrado
    if index == -1:
        return jsonify({"error": "Device not found"}), 404

    # Eliminar el dispositivo en la posición encontrada
    devices_data.pop(index)

    # Guardar la lista actualizada en el archivo JSON para persistencia
    with open("devices.json", "w") as f:
        json.dump(devices_data, f, indent=2)

    # Retornar mensaje de éxito con código HTTP 200 (OK)
    return jsonify({"message": "Device deleted successfully"}), 200



if __name__ == "__main__":
    app.run(debug=True)

    "añadir requirements.txt"