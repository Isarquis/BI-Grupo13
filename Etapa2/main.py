from fastapi import FastAPI
from DataModel import PredictionInput
from PredictionModel import predecir

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API de Fake News Detector Activa"}

app = FastAPI()

@app.post("/predict/")
def predict(input_data: PredictionInput):
    resultados = predecir(input_data.titulo, input_data.descripcion)
    return resultados

# Para ejecutar la API, usa: uvicorn main:app --reload
