# tecnologias web - Preparación AE1
# Pasos para la Ejecución del Proyecto

## 1. Descargar el Repositorio

https://github.com/MateoDelG/tecnologias-web

## 2. Crear un Entorno Virtual
Ejecuta el siguiente comando para crear un entorno virtual en Python:

```bash
python -m venv venv
```

## 3. Activar el Entorno Virtual
Para activar el entorno virtual, usa el siguiente comando:

```bash
source venv/Scripts/activate
```

## 4. Instalar las Dependencias
Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

## 5. Ejecutar el Script `devices_generator.py`
Para generar los datos de los dispositivos, ejecuta:

```bash
python devices_generator.py
```

## 6. Ejecutar la Aplicación
Para iniciar la aplicación, ejecuta:

```bash
python app.py
```

---

# **Pruebas de Endpoints**

## 7.1 Obtener la Lista de Dispositivos
**Endpoint:**  
`GET http://localhost:5000/devices`

**Respuesta esperada:**
```json
[
  {
    "id": 1,
    "name": "Device 1",
    "status": "inactive",
    "type": "speed"
  },
  {
    "id": 2,
    "name": "Device 2",
    "status": "active",
    "type": "temperature"
  }
]
```

---

## 7.2 Obtener un Dispositivo por ID
**Endpoint:**  
`GET http://localhost:5000/devices/1`

**Respuesta esperada:**
```json
{
  "id": 1,
  "name": "Device 1",
  "status": "inactive",
  "type": "speed"
}
```

---

## 7.3 Crear un Nuevo Dispositivo
**Endpoint:**  
`POST http://localhost:5000/devices`

**Body:**
```json
{
  "name": "Device POST test 1",
  "status": "inactive",
  "type": "speed"
}
```

**Respuesta esperada:**
```json
{
  "id": 12,
  "name": "Device POST test 1",
  "status": "inactive",
  "type": "speed"
}
```

---

## 7.4 Actualizar un Dispositivo
**Endpoint:**  
`PUT http://localhost:5000/devices/1`

**Body:**
```json
{
  "name": "Device PUT test 1",
  "status": "status changed",
  "type": "new type"
}
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "name": "Device PUT test 1",
  "status": "status changed",
  "type": "new type"
}
```

---

## 7.5 Eliminar un Dispositivo
**Endpoint:**  
`DELETE http://localhost:5000/devices/1`

**Respuesta esperada:**
```json
{
  "message": "Device deleted successfully"
}
```