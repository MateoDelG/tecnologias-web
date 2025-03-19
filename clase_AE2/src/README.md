# **📌 Pruebas Manuales con Postman**

Este documento describe cómo probar los endpoints de la API utilizando Postman.

## **🔹 1. Obtener todos los sensores (GET /sensores)**

### **Configuración en Postman**
* **Método**: GET
* **URL**: http://127.0.0.1:5000/sensores
* **Body**: ❌ No se envía body.

### **Esperado (Ejemplo de Respuesta)**
```json
[
    {
        "_id": "65f4a8b9e2d24a12b3456789",
        "tipo": "temperatura",
        "valor": 25,
        "ubicacion": "Planta 1",
        "fecha": "2025-03-17T12:00:00Z"
    }
]
```

## **🔹 2. Obtener sensores por tipo (GET /sensores/<tipo>)**

### **Configuración en Postman**
* **Método**: GET
* **URL**: http://127.0.0.1:5000/sensores/temperatura
* **Body**: ❌ No se envía body.

### **Esperado (Ejemplo de Respuesta)**
```json
[
    {
        "_id": "65f4a8b9e2d24a12b3456789",
        "tipo": "temperatura",
        "valor": 25,
        "ubicacion": "Planta 1",
        "fecha": "2025-03-17T12:00:00Z"
    }
]
```

## **🔹 3. Agregar un nuevo sensor (POST /sensores)**

### **Configuración en Postman**
* **Método**: POST
* **URL**: http://127.0.0.1:5000/sensores
* **Headers**:
   * Content-Type: application/json
* **Body** (Selecciona raw y tipo JSON):
```json
{
    "sensor_id": "sensor_123",
    "tipo": "presion",
    "valor": 250,
    "ubicacion": "Fábrica",
    "fecha": "2025-03-17T12:00:00Z"
}
```

### **Esperado (Ejemplo de Respuesta)**
```json
{
    "_id": "65f4a8b9e2d24a12b3456789",
    "tipo": "presion",
    "valor": 200,
    "ubicacion": "Taller",
    "fecha": "2025-03-17T12:00:00Z"
}
```

## **🔹 4. Actualizar un sensor (PUT /sensores/<tipo>)**

### **Configuración en Postman**
* **Método**: PUT
* **URL**: http://127.0.0.1:5000/sensores/presion
* **Headers**:
   * Content-Type: application/json
* **Body** (Selecciona raw y tipo JSON):
```json
{
    "valor": 320
}
```

### **Esperado (Ejemplo de Respuesta)**
```json
{
    "mensaje": "Sensor actualizado"
}
```

## **🔹 5. Eliminar un sensor (DELETE /sensores/<tipo>)**

### **Configuración en Postman**
* **Método**: DELETE
* **URL**: http://127.0.0.1:5000/sensores/presion
* **Body**: ❌ No se envía body.

### **Esperado (Ejemplo de Respuesta)**
```json
{
    "mensaje": "Sensor eliminado"
}
```

## **📌 Resumen de Pruebas en Postman**

| **Método** | **Ruta** | **Body** | **Esperado** |
|------------|----------|----------|--------------|
| GET | /sensores | ❌ | Lista de sensores |
| GET | /sensores/<tipo> | ❌ | Sensores del tipo especificado |
| POST | /sensores | ✅ JSON con sensor | Sensor agregado con _id |
| PUT | /sensores/<tipo> | ✅ JSON con datos a actualizar | "Sensor actualizado" |
| DELETE | /sensores/<tipo> | ❌ | "Sensor eliminado" |
