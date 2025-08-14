import json
import random


records = []
n: int = 1000
failure_rate: float = 0.05
# Nombre de fallades
failure_count = int(n * failure_rate)

for i in range(n):
    # Generem valors base
    vibration = round(random.uniform(0, 10), 2)
    electric_consumption = round(random.uniform(200, 5000), 2)
    surface_temperature = round(random.uniform(20, 90), 2)
    rpm = round(random.uniform(500, 5000), 2)
    water_pressure = round(random.uniform(3, 5), 2)
    flow_rate = round(random.uniform(2, 5), 2)
    runtime_seconds = round(random.uniform(1000, 1_000_000), 2)

    # Patró de fallada: alta vibració, alta temperatura, baix flux
    if i < failure_count:
        vibration = round(random.uniform(8, 10), 2)
        surface_temperature = round(random.uniform(80, 90), 2)
        flow_rate = round(random.uniform(2, 2.5), 2)
        label = 1
    else:
        label = 0

    records.append({
        "vibration": vibration,
        "electric_consumption": electric_consumption,
        "surface_temperature": surface_temperature,
        "rpm": rpm,
        "water_pressure": water_pressure,
        "flow_rate": flow_rate,
        "runtime_seconds": runtime_seconds,
        "label": label
    })

dataset= {"records": records}
with open("pump_failure_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)
print("Dataset de prova creat: pump_failure_dataset.json")
