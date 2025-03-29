# -*- coding: utf-8 -*-

# 1. Importación de librerías
import nltk
import pandas as pd
import numpy as np
import re, string, unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from imblearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import joblib
from sklearn.pipeline import FunctionTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report


# Descarga de recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')

stop_words_es = stopwords.words("spanish")

# 2. Carga de datos
file_path = "fake_news_spanish.csv"
data = pd.read_csv(file_path, sep=";", encoding="utf-8")

# 3. Preparación de los datos
stop_words = list(set(stopwords.words('spanish')))
stemmer = SnowballStemmer('spanish')

def preprocessing(text):
    if isinstance(text, float) or text is None:  # Manejo de valores NaN
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)  # Eliminar signos de puntuación
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')  # Quitar tildes
    words = word_tokenize(text)
    filtered_words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(filtered_words)

def preprocess_series(X):
    if isinstance(X, pd.Series):
        return X.astype(str).apply(preprocessing)
    else:
        return preprocessing(str(X))  # Convertir a string y aplicar directamente

data = data.dropna(subset=['Titulo', 'Descripcion', 'Label'])

# Eliminar duplicados basados en Titulo y Descripcion
data = data.drop_duplicates(subset=['Titulo', 'Descripcion'])
# Aplicar limpieza a título y descripción
data["Titulo"] = data["Titulo"].apply(preprocessing)
data["Descripcion"] = data["Descripcion"].apply(preprocessing)

# 4. Separación de variables
X_data = data['Titulo'] + ' ' + data['Descripcion']
y_data = data['Label']

# División de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0)

# Definición del pipeline con SMOTE
pipeline = Pipeline([
    ('preprocessor', FunctionTransformer(preprocess_series, validate=False)),  
    ('tfidf', TfidfVectorizer(max_features=5000, stop_words=stop_words_es)),
    ('smote', SMOTE(random_state=42)),
    ('classifier', RandomForestClassifier(n_estimators=30, random_state=42))
])

# Entrenar el modelo
pipeline.fit(X_train, y_train)

# Guardar el modelo
joblib.dump(pipeline, "modelo_fake_news.joblib")

y_pred = pipeline.predict(X_test)

# Calcular métricas
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')  # Usa 'weighted' para multiclase
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Mostrar resultados
print(f"🔹 Accuracy: {accuracy:.4f}")
print(f"🔹 Precision: {precision:.4f}")
print(f"🔹 Recall: {recall:.4f}")
print(f"🔹 F1-Score: {f1:.4f}")
