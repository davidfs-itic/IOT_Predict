# main.py
from fastapi import FastAPI
from datetime import datetime
from services import predictor, trainer, model_manager
from schemas.schemas import PredictInput, PredictOutput, TrainInput, TrainOutput, StatusOutput
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(title="Pump Failure Prediction API")

@app.on_event("startup")
async def startup_event():
    model_manager.load_active_model()
    

# --------- Predict endpoint ---------
@app.post("/predict", response_model=PredictOutput)
async def predict_endpoint(data: PredictInput):
    result = predictor.predict(data.dict())
    result.update({
        "model_version": model_manager.get_model_info()["model_version"],
        "model_file": model_manager.get_model_info()["model_file"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })
    return result

# --------- Train endpoint ---------
@app.post("/train", response_model=TrainOutput)
async def train_endpoint(data: TrainInput):
    result = trainer.train_model(data.dict())
    result["status"] = "success"
    return result

# --------- Status endpoint ---------
@app.get("/status", response_model=StatusOutput)
async def status_endpoint():
    info = model_manager.get_model_info()
    if not info:
        return StatusOutput(
            model_version="none",
            model_file="none"
        )
    # Si vols, aquí podríem incloure més estadístiques
    return StatusOutput(
        model_version=info["model_version"],
        model_file=info["model_file"]
    )
