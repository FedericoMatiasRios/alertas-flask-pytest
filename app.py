from flask import Flask, request, jsonify
import os
from flask_cors import CORS  # Import CORS from flask_cors

def create_app():
    app = Flask(__name__)
    CORS(app)
    # Almacén temporal para las alertas (puede ser sustituido por una base de datos en producción)
    alertas = []

    import sys
    print(sys.path)
    # Ruta raíz para proporcionar una respuesta simple
    @app.route('/')
    def index():
        return '¡La aplicación de alerta temprana está en funcionamiento!'

    # Ruta para recibir alertas desde la aplicación móvil
    @app.route('/api/alertas', methods=['POST'])
    def recibir_alerta():
        try:
            imagen = guardar_imagen(request.files.get('imagen'))  # Save the image and get its path
            ubicacion = request.form['ubicacion']
            latitud = request.form['latitud']
            longitud = request.form['longitud']
            descripcion = request.form['descripcion']

            nueva_alerta = {
                'imagen': imagen,
                'ubicacion': ubicacion,
                'latitud': latitud,
                'longitud': longitud,
                'descripcion': descripcion
            }
            alertas.append(nueva_alerta)

            return jsonify({'mensaje': 'Alerta recibida correctamente'}), 201

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Error interno en el servidor'}), 500

    # Ruta para obtener todas las alertas (para la aplicación web de administración)
    @app.route('/api/alertas', methods=['GET'])
    def obtener_alertas():
        return jsonify({'alertas': alertas})

    # Función para guardar la imagen en la carpeta 'uploads' y devolver su ruta
    def guardar_imagen(imagen):
        if imagen:
            upload_folder = os.path.abspath('uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            imagen_path = os.path.join(upload_folder, imagen.filename)
            imagen.save(imagen_path)
            return imagen_path
        else:
            return None

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)