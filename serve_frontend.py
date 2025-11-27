from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Ruta al directorio del frontend compilado
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend-tareas', 'dist', 'frontend-tareas', 'browser')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    else:
        return send_from_directory(FRONTEND_DIR, 'index.html')

if __name__ == '__main__':
    print(f"Sirviendo frontend desde: {FRONTEND_DIR}")
    app.run(host='0.0.0.0', port=4200, debug=False)
