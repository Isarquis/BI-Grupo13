from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_unica"  # Necesario para usar sesiones

# Ruta principal para mostrar el formulario
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    
    # Inicializar historial en sesión si no existe
    if "historial" not in session:
        session["historial"] = []

    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]

        # Llamar a la API FastAPI
        api_url = "http://127.0.0.1:8000/predict"
        payload = {"titulo": [titulo], "descripcion": [descripcion]}  # Asegurar que es una lista
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            resultado = response.json()  # Mantenerlo como lista
            
            # Agregar la predicción al historial
            session["historial"].append(resultado[0])
            session.modified = True  # Guardar cambios en sesión
        else:
            resultado = [{"prediccion": "Error", "probabilidad": [0, 0]}]  # Manejo de error

    return render_template("index.html", resultado=resultado, historial=session["historial"])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
