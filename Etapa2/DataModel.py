from pydantic import BaseModel
from typing import List

class PredictionInput(BaseModel):
    titulo: List[str]  # Lista de títulos de noticias
    descripcion: List[str]  # Lista de descripciones de noticias

class PredictionResponse(BaseModel):
    texto: str
    prediccion: str
    probabilidad: list  # Lista con las probabilidades de cada clase
