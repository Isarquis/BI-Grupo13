from fastapi import FastAPI
from DataModel import PredictionInput
from PredictionModel import predecir

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

@app.get("/")
def home():
    return {"message": "API de Fake News Detector Activa"}


@app.post("/predict/")
def predict(input_data: PredictionInput):
    resultados = predecir(input_data.titulo, input_data.descripcion)
    print("a",resultados)
    return resultados

# Para ejecutar la API, usa: uvicorn main:app --reload
