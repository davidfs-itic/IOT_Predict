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



class TrainOutput(BaseModel):
    status: str
    model_version: str
    model_name: str
    model_params: dict
    model_file: str
    trained_at: str
    accuracy: float
    f1_score: float

# --------- Status ---------
class StatusOutput(BaseModel):
    model_version: str
    model_file: str
    last_training: Optional[str] = None
    records_seen: Optional[int] = None
    accuracy: Optional[float] = None
    f1_score: Optional[float] = None

class ModelInfo(BaseModel):
    model_version: str
    model_name: str
    model_params: dict
    model_file: str
    scaler_file: str
    trained_at:str
    accuracy: float
    f1_score: float

