# services/trainer.py
import pickle
import pandas as pd
import numpy as np
import json
import sklearn

from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from schemas.schemas import PredictInput
from services.model_manager import save_new_model
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
from schemas.schemas import TrainInput, TrainOutput
from schemas.schemas import PredictInput  




def train_model(training_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entrena un nou model amb les dades proporcionades.
    training_data: ha de contenir 'records', una llista de dicts amb features i label
    """
    records = training_data.get("records")
    if not records or not isinstance(records, list):
        raise ValueError("Falten dades d'entrenament o format incorrecte.")


    data = pd.DataFrame(records)

    feature_names = list(PredictInput.model_fields.keys())

    X = data[feature_names].values
    y = data["label"].values

    # Validar que tenim les dades necessàries
    if X.size == 0 or y.size == 0:
        raise ValueError("Les dades d'entrenament estan buides.")

    # Validate data dimensions
    if X.shape[1] != len(feature_names):
        raise ValueError(f"Expected {len(feature_names)} features, got {X.shape[1]}")
    
    if len(X) != len(y):
        raise ValueError(f"Number of features ({len(X)}) doesn't match number of labels ({len(y)})")
    
    # Check if we have enough samples for train/test split
    if len(X) < 10:
        raise ValueError("Insufficient data for training. Need at least 10 samples.")


    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    # Model Training and Hyperparameter Tuning
    models = {
        'RandomForest': RandomForestClassifier(),
        'GradientBoosting': GradientBoostingClassifier(),
        'LogisticRegression': LogisticRegression(),
        'SVM': SVC(probability=True)
    }

    params = {
        'RandomForest': {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20]},
        'GradientBoosting': {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 1]},
        'LogisticRegression': {'C': [0.01, 0.1, 1, 10]},
        'SVM': {'C': [0.01, 0.1, 1, 10], 'kernel': ['linear', 'rbf']}
    }

    best_models = {}
    best_accuracy = 0
    best_f1 = 0
    best_model_name = ''
    best_model = None

    for model_name in models.keys():
        grid = GridSearchCV(models[model_name], params[model_name], cv=5, n_jobs=-1, verbose=1)
        grid.fit(X_train, y_train)
        best_models[model_name] = grid.best_estimator_
        print(f"Best parameters for {model_name}: {grid.best_params_}")
        y_pred = grid.best_estimator_.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Accuracy for {model_name}: {accuracy}")
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_f1 = f1_score(y_test, y_pred)
            best_model_name = model_name
            best_model = grid.best_estimator_

    print(f"\nBest model: {best_model_name} with accuracy: {best_accuracy}")
    # Guardar nou model i obtenir info
    version, model_file,scaler_file = save_new_model(best_model,scaler)


    return {
        "model_version": version,
        "model_name": best_model_name,
        "model_params": best_models[best_model_name].get_params(),
        "model_file": str(model_file),
        "trained_at": datetime.utcnow().isoformat(),
        "accuracy": best_accuracy,
        "f1_score": best_f1
    }
