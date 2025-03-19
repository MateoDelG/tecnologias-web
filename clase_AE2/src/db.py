# db.py - Manejo de base de datos
from pymongo import MongoClient
from bson import ObjectId  # Para convertir ObjectId a string
"""MongoClient: Se usa para conectar a una base de datos MongoDB.
ObjectId: MongoDB usa un identificador único llamado ObjectId, que no es directamente serializable a JSON, por lo que lo convertimos a str."""

# Conectar a MongoDB
db_client = MongoClient("mongodb://localhost:27017/")
db = db_client["monitoreo_industrial"]
"""Se crea un cliente MongoDB que se conecta al servidor local en el puerto 27017 (puerto por defecto de MongoDB).
Se selecciona la base de datos monitoreo_industrial. Si no existe, MongoDB la creará automáticamente.
"""

# Definir colecciones
sensores = db["sensores"]
"""Se obtiene la colección sensores, que es donde se almacenarán los documentos de los sensores."""

tipos_validos = ["temperatura", "presion", "vibracion"]
rangos_validos = {
    "temperatura": (-10, 100),
    "presion": (0, 500),
    "vibracion": (0, 5),
}
"""tipos_validos: Lista de los únicos tipos de sensores aceptados.
rangos_validos: Diccionario con los rangos permitidos de cada tipo de sensor."""

def obtener_sensores():
    """Busca todos los documentos en la colección sensores.
    Convierte cada ObjectId a str para que sea JSON serializable.
    Devuelve una lista de sensores."""
    sensores_lista = []  # Creamos una lista vacía para almacenar los sensores

    for sensor in sensores.find():  # Iteramos sobre cada sensor obtenido de MongoDB
        sensor["_id"] = str(sensor["_id"])  # Convertimos el ObjectId en string
        sensores_lista.append(sensor)  # Agregamos el sensor modificado a la lista

    return sensores_lista  # Retornamos la lista con todos los sensores modificados

def obtener_sensores_por_tipo(tipo):
    """Verifica si el tipo es válido.
    Filtra los sensores por tipo en la base de datos.
    Retorna la lista de sensores filtrados o None si el tipo no es válido."""
    if tipo not in tipos_validos:
        return None
    sensores_lista = []  # 1️⃣ Creamos una lista vacía para almacenar los sensores filtrados

    for sensor in sensores.find({"tipo": tipo}):  # 2️⃣ Buscamos sensores que tengan el tipo especificado
        sensor["_id"] = str(sensor["_id"])  # 3️⃣ Convertimos el ObjectId a un string
        sensores_lista.append(sensor)  # 4️⃣ Agregamos el sensor modificado a la lista

    return sensores_lista  # 5️⃣ Devo

def agregar_sensor(sensor):
    """Agrega un nuevo sensor si el sensor_id no está repetido."""
    
    # Extraemos los datos del sensor
    sensor_id = sensor.get("sensor_id")
    tipo = sensor.get("tipo")
    valor = sensor.get("valor")
    ubicacion = sensor.get("ubicacion")
    fecha = sensor.get("fecha")

    # Validaciones básicas
    if not sensor_id or tipo not in tipos_validos or not ubicacion or not fecha:
        return None  # Si falta algún dato, devolvemos None
    
    # Verificar si ya existe un sensor con el mismo sensor_id
    if sensores.find_one({"sensor_id": sensor_id}):
        return "EXISTE"  # Devolvemos "EXISTE" si el sensor ya está registrado

    # Validar que el valor esté dentro del rango permitido
    if not (rangos_validos[tipo][0] <= valor <= rangos_validos[tipo][1]):
        return None  # Si el valor está fuera del rango, devolvemos None

    # Insertamos el sensor en la base de datos
    resultado = sensores.insert_one(sensor)

    # Convertimos el ID generado por MongoDB a string para compatibilidad con JSON
    sensor["_id"] = str(resultado.inserted_id)

    return sensor  # Retornamos el sensor con su nuevo _id

def actualizar_sensor(sensor_id, datos_actualizados):
    """Busca el sensor por sensor_id y actualiza solo los campos enviados.
    Devuelve True si se actualizó correctamente o False si no encontró el sensor."""
    
    resultado = sensores.update_one({"sensor_id": sensor_id}, {"$set": datos_actualizados})
    
    return resultado.matched_count > 0  # Devuelve True si encontró y actualizó

def eliminar_sensor(sensor_id):
    """Busca el sensor por sensor_id y lo elimina.
    Retorna True si se eliminó correctamente o False si no se encontró."""
    
    resultado = sensores.delete_one({"sensor_id": sensor_id})
    
    return resultado.deleted_count > 0  # Devuelve True si eliminó el sensor

def eliminar_todos_los_sensores():
    """Elimina todos los sensores de la base de datos.
    Retorna True si se eliminaron sensores, False si no había ninguno."""
    
    resultado = sensores.delete_many({})  # Elimina todos los documentos en la colección

    return resultado.deleted_count > 0  # Devuelve True si eliminó al menos un sensor
