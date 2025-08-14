# services/predictor.py
import pickle
from pathlib import Path
from typing import Dict, Any
from pump_failure_service.services import model_manager

MODEL_PATH = Path("models/model_actual.pkl")


def predict(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Realitza una predicció amb el model actiu.
    input_data: diccionari amb les dades de entrada.
    Retorna: diccionari amb predicció i informació addicional.
    """

    
    if model_manager.model is None:
        raise RuntimeError("Model no carregat. Crida primer model_manager.load_model()")

    model=model_manager.model
    scaler=model_manager.scaler

    # TODO: Preprocessar input_data segons el que espera el model
    features = [
        input_data.get("vibration"),
        input_data.get("electric_consumption"),
        input_data.get("surface_temperature"),
        input_data.get("rpm"),
        input_data.get("water_pressure"),
        input_data.get("flow_rate"),
        input_data.get("runtime_seconds")
    ]

    features_scaled = scaler.transform([features])

    # TODO: Depenent del model, potser cal convertir a np.array
    prediction = model.predict([features_scaled])[0]
    probability = getattr(model, "predict_proba", lambda x: None)([features_scaled])

    return {
        "prediction": prediction,
        "probability": probability.tolist() if probability is not None else None
    }
