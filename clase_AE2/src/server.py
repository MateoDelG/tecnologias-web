from flask import Flask
from routes import routes
"""Flask: Importamos Flask para crear la aplicación web.
routes: Importamos las rutas definidas en routes.py."""

app = Flask(__name__) 
"""Se crea una instancia de Flask, que es la aplicación web.
__name__ se usa para indicar que este es el módulo principal."""


app.register_blueprint(routes)
"""register_blueprint(routes):
Flask usa "blueprints" para modularizar la API.
Aquí se agregan todas las rutas definidas en routes.py."""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
"""if __name__ == "__main__": Se asegura de que este script se ejecute solo si es el principal (no si es importado como módulo).
app.run(debug=True, port=5000):
debug=True:
Recarga automáticamente la aplicación si detecta cambios en el código.
Muestra errores detallados en el navegador.
port=5000: La API se ejecutará en http://127.0.0.1:5000/."""