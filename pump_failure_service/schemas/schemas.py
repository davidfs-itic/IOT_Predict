# models/schemas.py
from pydantic import BaseModel
from typing import List, Optional

# --------- Predict ---------
class PredictInput(BaseModel):
    vibration: float
    electric_consumption: float
    surface_temperature: float
    rpm: float
    water_pressure: float
    flow_rate: float
    runtime_seconds: float

class PredictOutput(BaseModel):
    prediction: int
    probability: Optional[List[float]] = None
    model_info: Optional[dict] = None

# --------- Train ---------
class TrainInput(BaseModel):
    records: List[dict]  # Cada dict ha de tenir les claus de PredictInput + 'label'


#------------ Info ------------

class ModelInfo(BaseModel):
    model_version: str
    model_name: str
    model_params: dict
    model_file: str
    scaler_file: str
    trained_at:str
    accuracy: float
    f1_score: float

class TrainOutput(BaseModel):
    status: str
    model: ModelInfo