from flask import request
from flask import Flask, jsonify
import json, os
from flask_cors import CORS # pip install flask-cors
app = Flask(__name__)
CORS(app) # Necesario en desarrollo si el frontend está en OTRO origen (puerto/dominio). 
           # Sin esto, el navegador bloquea la petición por CORS (Postman no se ve afectado).
STORAGE = "storage.json"
global tareas
tareas = []
def cargar():
    
    if os.path.exists(STORAGE):
        with open(STORAGE, "r", encoding="utf-8") as f:
            tareas[:] = json.load(f)

def guardar():
    with open(STORAGE, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

# tareas = [
#     {"id": 1, "titulo": "Aprender Flask", "hecha": False},
#     {"id": 2, "titulo": "Practicar requests", "hecha": True}
# ]
@app.get("/")
def home():
    return jsonify({"mensaje": "API de Tareas – Nivel 3 lista"})

@app.get("/tareas")
def obtener_tareas():
    return jsonify(tareas), 200

@app.get("/tareas/<int:tid>")#aca hemos quedado
def obtener_tarea(tid):
    tarea = next((t for t in tareas if t["id"] == tid), None)  # next busca el primer elemento que cumple la condicion
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(tarea), 200
@app.post("/tareas")
def crear_tarea():
    data = request.get_json(silent=True) or {}
    titulo = (data.get("titulo") or "").strip()
    if not titulo:
        return jsonify({"error": "El campo 'titulo' es requerido"}), 400

    nuevo_id = max([t["id"] for t in tareas] + [0]) + 1
    nueva = {"id": nuevo_id, "titulo": titulo, "hecha": bool(data.get("hecha", False))}
    tareas.append(nueva)
    guardar()
    return jsonify(nueva), 201
@app.put("/tareas/<int:tid>")
def actualizar_tarea(tid):
    tarea = next((t for t in tareas if t["id"] == tid), None)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    data = request.get_json(silent=True) or {}
    if "titulo" in data:
        nuevo_titulo = (data.get("titulo") or "").strip()
        if not nuevo_titulo:
            return jsonify({"error": "El título no puede ser vacío"}), 400
        tarea["titulo"] = nuevo_titulo
    if "hecha" in data:
        tarea["hecha"] = bool(data["hecha"])
    guardar()
    return jsonify(tarea), 200

# Eliminar una tarea para hoy 5/11
@app.delete("/tareas/<int:tid>")
def borrar_tarea(tid):
    global tareas
    if not any(t["id"] == tid for t in tareas):
        return jsonify({"error": "Tarea no encontrada"}), 404
    tareas = [t for t in tareas if t["id"] != tid]
    guardar()
    return jsonify({"mensaje": f"Tarea {tid} eliminada"}), 200

if __name__ == "__main__":
    cargar()
    app.run(debug=True)