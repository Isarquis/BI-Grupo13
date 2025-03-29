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
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE
import joblib
from sklearn.pipeline import FunctionTransformer

# Descarga de recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')

stop_words_es = stopwords.words("spanish")
stop_words = list(set(stopwords.words('spanish')))
stemmer = SnowballStemmer('spanish')

def preprocessing(text):
    if isinstance(text, float) or text is None:
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    words = word_tokenize(text)
    filtered_words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(filtered_words)

def preprocess_series(X):
    if isinstance(X, pd.Series):
        return X.astype(str).apply(preprocessing)
    else:
        return preprocessing(str(X))

def reentrenar_modelo(nuevo_df):
    # Cargar el modelo previamente entrenado
    modelo_previo = joblib.load("modelo_fake_news.joblib")
    
    # Cargar los datos previos usados en el entrenamiento
    modelo_previo_df = pd.read_csv("fake_news_spanish.csv", sep=";", encoding="utf-8")
    
    # Unir los datos previos con los nuevos
    data_combinada = pd.concat([modelo_previo_df, nuevo_df], ignore_index=True)
    # Eliminar filas con NaN en cualquier columna relevante
    data_combinada = data_combinada.dropna(subset=['Titulo', 'Descripcion', 'Label'])

    # Eliminar duplicados basados en Titulo y Descripcion
    data_combinada = data_combinada.drop_duplicates(subset=['Titulo', 'Descripcion'])


    data_combinada["Titulo"] = data_combinada["Titulo"].apply(preprocessing)
    data_combinada["Descripcion"] = data_combinada["Descripcion"].apply(preprocessing)
    
    X_data = data_combinada['Titulo'] + ' ' + data_combinada['Descripcion']
    y_data = data_combinada['Label']
    
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0)
    
    pipeline = Pipeline([
        ('preprocessor', FunctionTransformer(preprocess_series, validate=False)),  
        ('tfidf', TfidfVectorizer(max_features=5000, stop_words=stop_words_es)),
        ('smote', SMOTE(random_state=42)),
        ('classifier', RandomForestClassifier(n_estimators=30, random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, "modelo_fake_news.joblib")
    
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    return accuracy, precision, recall, f1
