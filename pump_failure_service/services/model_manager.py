# services/model_manager.py
import pickle
from pathlib import Path
from datetime import datetime

MODELS_DIR = Path("models/")
MODELS_DIR.mkdir(exist_ok=True)

# ------------------------------
# Variables globals del model
# ------------------------------
model = None
scaler = None
model_version = None
model_file = None
scaler_file = None

# ------------------------------
# Desa un nou model amb scaler
# ------------------------------
def save_new_model(new_model, new_scaler) -> (str, Path, Path):
    """
    Desa un nou model amb número de versió i actualitza el model actiu.
    Retorna: (versió, ruta del model, ruta del scaler)
    """
    global model, scaler, model_version, model_file, scaler_file

    # Generar número de versió simple amb data
    version = datetime.utcnow().strftime("v%Y%m%d_%H%M%S")
    model_path = MODELS_DIR / f"pump_failure_model_{version}.pkl"
    scaler_path = MODELS_DIR / f"pump_failure_scaler_{version}.pkl"

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

    # Actualitza variables globals
    model = new_model
    scaler = new_scaler
    model_version = version
    model_file = model_path
    scaler_file = scaler_path

    # Guarda informació resumida
    with open(MODELS_DIR / "model_info.json", "w") as f:
        f.write(f'{{"model_version": "{version}", "model_file": "{model_file}", "scaler_file": "{scaler_file}"}}')

    with open(MODELS_DIR / "model_active.txt", "w") as f:
        f.write(f"{version}\n{model_file}\n{scaler_file}")

    return version, model_path, scaler_path

# ------------------------------
# Carrega el model actiu
# ------------------------------
def load_active_model():
    """
    Carrega el model i scaler actius a les variables globals.
    """
    global model, scaler, model_version, model_file, scaler_file

    model_actual = MODELS_DIR / "model_actual.pkl"
    scaler_actual = MODELS_DIR / "scaler_actual.pkl"
    if not model_actual.exists() or not scaler_actual.exists():
        print("No hi ha cap model actiu per carregar.")
        return False

    with open(model_actual, "rb") as f:
        model = pickle.load(f)
    with open(scaler_actual, "rb") as f:
        scaler = pickle.load(f)

    model_file = model_actual
    scaler_file = scaler_actual
    model_version = model_actual.stem.replace("pump_failure_model_", "")

    print(f"Model actiu carregat: {model_file}, versió {model_version}")
    return True

# ------------------------------
# Retorna informació del model
# ------------------------------
def get_model_info():
    """
    Retorna informació del model actiu.
    """
    return {
        "model_version": model_version,
        "model_file": str(model_file) if model_file else None,
        "scaler_file": str(scaler_file) if scaler_file else None
    }
