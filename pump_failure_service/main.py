# main.py
import json
from fastapi import FastAPI
from datetime import datetime
from services import predictor, trainer, model_manager
from schemas.schemas import ModelInfo, PredictInput, PredictOutput, TrainInput, TrainOutput
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(title="Pump Failure Prediction API")

@app.on_event("startup")
async def startup_event():
   global info
   if model_manager.load_active_model():
       print(f"Model actiu carregat: {json.dumps(model_manager.get_model_info(), indent=4)}")


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
    try:
        model = trainer.train_model(data.model_dump())
        result = {
            "status": "success",
            "model": model
        }
    except Exception as e:
        logger.error(f"Error during training: {e}")
        result = {
            "status": "error:" + str(e),
            "model": None
        }
    return result

# --------- Status endpoint ---------
@app.get("/model_info", response_model=ModelInfo)
async def status_endpoint():

    if not model_manager.get_model_info():
        return ModelInfo(
            model_version="Not trained",
            model_file="",
            scaler_file="",
            trained_at="",
            accuracy=0.0,
            f1_score=0.0
        )
        
    return model_manager.get_model_info()
