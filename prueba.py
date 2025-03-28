import joblib
import pandas as pd
from intento import preprocess_series

# Cargar el modelo guardado
modelo_cargado = joblib.load("modelo_fake_news.joblib")

# Verificar que se cargó correctamente
print("Modelo cargado correctamente.")

# Definir ejemplos de prueba
ejemplos = ["El 'Ahora o nunca' de Joan Fuster sobre el estatuto valenciano cumple 40 años. El valencianismo convoca en Castelló su fiesta grande en conmemoración del mítico Aplec de la plaza de toros de la capital de La Plana, en plena batalla por el estatuto."]

# Convertir a pandas.Series para que sea compatible con la transformación
ejemplos_series = pd.Series(ejemplos)

# Aplicar preprocesamiento antes de hacer la predicción
ejemplos_procesados = preprocess_series(ejemplos_series)

# Realizar predicciones
predicciones = modelo_cargado.predict(ejemplos_procesados)

# Mostrar resultados
for i, ejemplo in enumerate(ejemplos):
    print(f"Texto: {ejemplo}")
    print(f"Predicción: {'Falso' if predicciones[i] == 0 else 'Verdadero'}\n")
