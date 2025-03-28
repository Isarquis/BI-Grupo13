from DataModel import PredictionInput, PredictionResponse, RetrainInput, RetrainResponse
from PredictionModel import predecir
from RetrainModel import reentrenar_modelo
from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API de Fake News Detector Activa"}

app = FastAPI()

@app.post("/predict/")
def predict(input_data: PredictionInput):
    resultados = predecir(input_data.titulo, input_data.descripcion)
    return resultados

@app.post("/retrain/")
async def retrain(file: UploadFile = File(...)):  # File ahora está correctamente importado
    df = pd.read_csv(file.file, sep=";", encoding="utf-8")
    
    # Llamar la función de reentrenamiento
    accuracy, precision, recall, f1 = reentrenar_modelo(df)

    return {
        "mensaje": "Modelo actualizado con éxito.",
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }
