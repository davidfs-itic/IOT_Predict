# services/model_manager.py
import json
import pickle
from pathlib import Path
from datetime import datetime

from schemas.schemas import ModelInfo

MODELS_DIR = Path("models/")
MODELS_DIR.mkdir(exist_ok=True)

# ------------------------------
# Variables globals del model
# ------------------------------
model = None
scaler = None
info = None
# ------------------------------
# Desa un nou model amb scaler
# ------------------------------
def save_new_model(new_model, new_scaler,model_info) -> (bool):
    """
    Desa un nou model amb número de versió i actualitza el model actiu.
    Retorna: (versió, ruta del model, ruta del scaler)
    """
    global model, scaler, info

    # Generar número de versió simple amb data
    version = datetime.utcnow().strftime("v%Y%m%d_%H%M%S")
    model_path = MODELS_DIR / f"pump_failure_model_{version}.pkl"
    scaler_path = MODELS_DIR / f"pump_failure_scaler_{version}.pkl"
    info_path = MODELS_DIR / "model_info.json"

    # Desa els fitxers
    with open(model_path, "wb") as f:
        pickle.dump(new_model, f)
    with open(scaler_path, "wb") as f:
        pickle.dump(new_scaler, f)


    # Actualitza fitxers actius
    model_actual = MODELS_DIR / "model_actual.pkl"
    scaler_actual = MODELS_DIR / "scaler_actual.pkl"
    if model_actual.exists():
        model_actual.unlink()
    if scaler_actual.exists():
        scaler_actual.unlink()
    model_actual.symlink_to(model_path.resolve())
    scaler_actual.symlink_to(scaler_path.resolve())

    model_info.model_version = version
    model_info.model_file = str(model_path)
    model_info.scaler_file = str(scaler_path)

    with open(info_path, "w") as f:
        json.dump(model_info.dict(), f, indent=4)
        
    # Actualitza variables globals
    model = new_model
    scaler = new_scaler
    info = model_info

    return True

# ------------------------------
# Carrega el model actiu
# ------------------------------
def load_active_model() -> bool:
    """
    Carrega el model i scaler actius a les variables globals.
    """
    global model, scaler, info

    model_actual = MODELS_DIR / "model_actual.pkl"
    scaler_actual = MODELS_DIR / "scaler_actual.pkl"
    info_actual = MODELS_DIR / "model_info.json"

    if not model_actual.exists() or not scaler_actual.exists():
        print("No hi ha cap model actiu per carregar.")
        return False

    with open(model_actual, "rb") as f:
        model = pickle.load(f)
    with open(scaler_actual, "rb") as f:
        scaler = pickle.load(f)

    with open(info_actual, "r") as f:
        info = json.load(f)

    return True

# ------------------------------
# Afegim una funció per retornar la informació del model
# ------------------------------
def get_model_info():
    return info