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
│── testing/
│   ├── data_generator.py
│   └── pump_failure_dataset.json
└── models/   ← carpeta on es guarden els arxius .pkl
```

L'arxiu pump_failure_dataset.json té un json preparar per utilitzar en la funció train.



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
  "probability": [0.05, 0.95]
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
# todo
```

### Endpoint status:
Sortida
```
# todo
```

## Per provar l'aplicació en local (Sense docker):

Des de la carpeta pump_failure_service:

Crear entorn virual
```
python3 -m venv .venv
source .venv/bin/activate
```

Instal·lar requeriments:
```
pip install -r requirements.txt
```

Executar la app
```
uvicorn main:app --host 0.0.0.0 --port 8443 --ssl-keyfile ssl/key.pem --ssl-certfile ssl/cert.pem --reload 
```