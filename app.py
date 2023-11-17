from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Ruta al archivo JSON
JSON_FILE_PATH = 'conversaciones.json'

# Intentar cargar el diccionario desde el archivo JSON
try:
    with open(JSON_FILE_PATH, 'r') as json_file:
        conversaciones = json.load(json_file)
except FileNotFoundError:
    conversaciones = {}

def guardar_conversaciones():
    # Guardar el diccionario en el archivo JSON
    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(conversaciones, json_file, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/guide")
def guide_page():
    return render_template("guide.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]

    # Buscar una pregunta similar en el diccionario
    matches = get_close_matches(user_message, conversaciones.keys(), n=1, cutoff=0.8)

    if matches:
        response = conversaciones[matches[0]]
    else:
        # Si no hay coincidencia cercana, preguntar si desea aprender sobre la pregunta
        response = f"Lo siento, no entiendo eso. ¿Te gustaría enseñarme más sobre la pregunta '{user_message}'? (Sí/No)"

    return jsonify({"response": response, "question": user_message})

@app.route("/learn", methods=["POST"])
def learn():
    user_message = request.form["user_message"]
    new_response = request.form["new_response"]

    # Aprender de la nueva pregunta y respuesta si el usuario desea enseñar
    if request.form.get("learn") == "yes":
        conversaciones[user_message] = new_response
        guardar_conversaciones()

    return jsonify({"message": "¡Gracias por enseñarme!"})

@app.route("/get_conversations", methods=["GET"])
def get_conversations():
    return jsonify(conversaciones)

if __name__ == "__main__":
    app.run(debug=True)
