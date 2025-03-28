from pydantic import BaseModel
from typing import List

class PredictionInput(BaseModel):
    titulo: List[str]  # Lista de títulos de noticias
    descripcion: List[str]  # Lista de descripciones de noticias

class PredictionResponse(BaseModel):
    texto: str
    prediccion: str
    probabilidad: list  # Lista con las probabilidades de cada clase

class RetrainInput(BaseModel):
    titulo: List[str]
    descripcion: List[str]
    etiqueta: List[int]  # Etiquetas reales (0 = Falso, 1 = Verdadero)

class RetrainResponse(BaseModel):
    mensaje: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float