from DataModel import PredictionInput, PredictionResponse, RetrainInput, RetrainResponse
from PredictionModel import predecir
from RetrainModel import reentrenar_modelo
from fastapi import FastAPI, UploadFile, File, Body
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from io import StringIO
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import json
# Importar la función de predicción desde PredictionModel.py
from PredictionModel import predecir  

app = FastAPI()
@app.get("/")
def home():
    return {"message": "API de Fake News Detector Activa"}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

@app.post("/predict/")
def predict(input_data: PredictionInput):
    resultados = predecir(input_data.titulo, input_data.descripcion)
    return resultados

@app.post("/retrain/")
async def retrain(file: UploadFile = File(...)):  # File ahora está correctamente importado
    df = pd.read_csv(file.file, sep=";", encoding="utf-8")
    
    # Llamar la función de reentrenamiento
    accuracy, precision, recall, f1 = reentrenar_modelo(df)
    print({
        "mensaje": "Modelo actualizado con éxito.",
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    })
    return {
        "mensaje": "Modelo actualizado con éxito.",
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }
