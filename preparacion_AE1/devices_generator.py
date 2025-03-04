import json
import random

def generate_devices_json(num_entries=5, filename="devices.json"):
    """
    Genera un archivo JSON con 'num_entries' dispositivos de ejemplo.
    
    :param num_entries: Cantidad de dispositivos a generar.
    :param filename: Nombre del archivo JSON que se creará o sobreescribirá.
    """
    
    device_types = ["temperature", "pressure", "speed"]
    device_status = ["active", "inactive"]
    
    devices = []
    
    for i in range(1, num_entries + 1):
        device = {
            "id": i,
            "name": f"Device {i}",
            "type": random.choice(device_types),
            "status": random.choice(device_status)
        }
        devices.append(device)
    
    # Guardar la lista de dispositivos en el archivo JSON
    with open(filename, "w") as f:
        json.dump(devices, f, indent=2)
    
    print(f"Se han generado {num_entries} dispositivos en el archivo '{filename}'.")


# Ejemplo de uso:
if __name__ == "__main__":
    # Genera 10 dispositivos aleatorios en un archivo llamado "devices.json"
    generate_devices_json(num_entries=10, filename="devices.json")