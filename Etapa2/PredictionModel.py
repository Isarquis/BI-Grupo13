import joblib
import pandas as pd
from intento import preprocess_series
# Cargar el modelo guardado
modelo = joblib.load("modelo_fake_news.joblib")

def predecir(titulos, descripciones):
    # Unir título y descripción
    textos_completos = [f"{t} {d}" for t, d in zip(titulos, descripciones)]
    
    textos_series =pd.Series(textos_completos)
    predicciones = modelo.predict(textos_series).tolist()  # Predicciones binarias (0 o 1)
    probabilidades = modelo.predict_proba(textos_series).tolist()  # Probabilidad de cada clase
    
    # Formatear resultados
    resultados = [
        {
            "titulo": t,
            "descripcion": d,
            "prediccion": "Verdadero" if p == 1 else "Falso",
            "probabilidad": prob
        }
        for t, d, p, prob in zip(titulos, descripciones, predicciones, probabilidades)
    ]
    
    return resultados