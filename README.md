# Projecte prediccio fallades dispositiu IOT
Prova de concepte. 
S'entrena un model de fallades en aquest cas d'una bomba d'aigua.
Es mesuren els seguents valors, i es fa una prediccio.

    vibration: float
    electric_consumption: float
    surface_temperature: float
    rpm: float
    water_pressure: float
    flow_rate: float
    runtime_seconds: float

Codi basat en [Aquest notebook de kaggle](https://www.kaggle.com/code/muhammadfaizan65/machine-failure-prediction-eda-modeling/notebook)

 ## Estrucutura del projecte
 ```
project/
│── main.py
│── requirements.txt
│── schemas/
│   └── schemas.py
│── services/
│   ├── predictor.py
│   ├── trainer.py
│   └── model_manager.py
└── models/   ← carpeta on es guarden els arxius .pkl
```

## Diagrama sequencia
### Predict:
```
Dispositiu IoT       Broker MQTT       Node-RED                  Servei Python ML
     |                   |                 |                             |
     |--- Mesura ------->|                 |                             |
     |                   |--- Pub/Sub ---->|                             |
     |                   |                 |--- POST /predict ---------->|
     |                   |                 |   (JSON amb features)       |
     |                   |                 |                             |
     |                   |                 |<-- JSON resposta -----------|
     |                   |                 |  (fallada_prob, label)      |
     |                   |                 |                             |
     |                   |                 |--- Desa InfluxDB/avisa sms->|
     |                   |                 |                       |
```
### Train:
```
Admin / Script        Node-RED                Servei Python ML
     |                   |                           |
     |--- Ordre train --->|                          |
     |                   |--- POST /train ---------->|
     |                   |   (JSON: rang dates o     |
     |                   |    dades inline)          |
     |                   |                           |
     |                   |<-- JSON resposta ---------|
     |                   |  (status, version, msg)   |
     |                   |                           |
     |                   |--- Notificació Email ---->|
```

## Us dels json:
### Endpoint predict:
Entrada:
```
{
  "vibration": 0.12,
  "electric_consumption": 450.5,
  "surface_temperature": 65.2,
  "rpm": 1480,
  "water_pressure": 3.4,
  "flow_rate": 20.5,
  "runtime_seconds": 3600
}
```

Sortida:
 ```
 {
  "prediction": 1,
  "probability": [0.05, 0.95],
  "model_version": "v20250813_120045",
  "model_file": "/models/pump_failure_model_v20250813_120045.pkl",
  "timestamp": "2025-08-13T14:32:10Z"
}
```

### Endpoint train:
Entrada
```
[
  {
    "vibracio": 8.56,
    "consum": 476.0,
    "temperatura": 69.1,
    "revolucions": 1670.0,
    "pressio": 3.66,
    "flux": 2.74,
    "temps_arrencada": 283216.9,
    "fallada": 0
  },
  ...
]

```
Sortida
```
{
  "status": "success",
  "model_version": "v20250813_120045",
  "model_file": "/models/pump_failure_model_v20250813_120045.pkl",
  "trained_at": "2025-08-13T14:35:50Z",
  "accuracy": 0.94,
  "f1_score": 0.92
}
```

### Endpoint status:
Sortida
```
{
  "model_version": "v20250813_120045",
  "model_file": "/models/pump_failure_model_v20250813_120045.pkl",
  "last_training": "2025-08-13T14:35:50Z",
  "records_seen": 10523,
  "accuracy": 0.94,
  "f1_score": 0.92
}
```