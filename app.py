from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime, timedelta

app = FastAPI()


class VoltageData(BaseModel):
    timestamp: str
    voltage: float
    temperature: float
    current: float
    engine_rpm: int
    vehicle_speed: float
    fuel_level: float
    status: str
    status_message: str


class VoltageResponse(BaseModel):
    data: List[VoltageData]


class VoltageAlert(BaseModel):
    timestamp: str
    voltage: float
    status: str
    alert_message: str


class VehicleTypeData(BaseModel):
    vehicle_type: str
    count: int


class VehicleSpecs(BaseModel):
    vehicle_type: str
    horsepower: int
    torque: int
    weight: int


class VoltageThreshold(BaseModel):
    lower_bound: float
    upper_bound: float


# Configuration for voltage thresholds
voltage_threshold = VoltageThreshold(lower_bound=12.0, upper_bound=14.0)


# Generate synthetic voltage data
def generate_voltage_data(num_records: int) -> List[VoltageData]:
    data = []
    base_time = datetime.now()
    for i in range(num_records):
        timestamp = (base_time - timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M:%SZ')
        voltage = round(random.uniform(10.0, 16.0), 2)
        temperature = round(random.uniform(-20.0, 50.0), 2)
        current = round(random.uniform(0.0, 100.0), 2)
        engine_rpm = random.randint(0, 7000)
        vehicle_speed = round(random.uniform(0, 200), 2)
        fuel_level = round(random.uniform(0, 100), 2)
        status = "OK" if voltage_threshold.lower_bound <= voltage <= voltage_threshold.upper_bound else "Fault"
        status_message = "Normal operation" if status == "OK" else "Voltage out of range"

        if status == "Fault":
            if voltage < voltage_threshold.lower_bound:
                status_message = "Voltage too low"
            elif voltage > voltage_threshold.upper_bound:
                status_message = "Voltage too high"

        data.append(VoltageData(
            timestamp=timestamp,
            voltage=voltage,
            temperature=temperature,
            current=current,
            engine_rpm=engine_rpm,
            vehicle_speed=vehicle_speed,
            fuel_level=fuel_level,
            status=status,
            status_message=status_message
        ))
    return data


# Generate synthetic vehicle type data
def generate_vehicle_type_data() -> List[VehicleTypeData]:
    vehicle_types = ["Cybertruck", "Model 3", "Model S"]
    data = [VehicleTypeData(vehicle_type=vt, count=random.randint(10, 100)) for vt in vehicle_types]
    return data


# Generate synthetic vehicle specs
def generate_vehicle_specs() -> List[VehicleSpecs]:
    specs = [
        VehicleSpecs(vehicle_type="Cybertruck", horsepower=800, torque=1000, weight=6000),
        VehicleSpecs(vehicle_type="Model 3", horsepower=450, torque=470, weight=3500),
        VehicleSpecs(vehicle_type="Model S", horsepower=670, torque=800, weight=4500)
    ]
    return specs


# FastAPI endpoints
@app.get("/voltage", response_model=VoltageResponse)
def get_voltage_data(records: int = 100):
    if records <= 0:
        raise HTTPException(status_code=400, detail="Number of records must be greater than 0")
    data = generate_voltage_data(records)
    return VoltageResponse(data=data)


@app.get("/voltage/{timestamp}", response_model=VoltageData)
def get_voltage_by_timestamp(timestamp: str):
    data = generate_voltage_data(1000)
    for record in data:
        if record.timestamp == timestamp:
            return record
    raise HTTPException(status_code=404, detail="Timestamp not found")


@app.get("/voltage/range", response_model=VoltageResponse)
def get_voltage_data_range(start_time: str, end_time: str):
    try:
        start_dt = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
        end_dt = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use ISO format YYYY-MM-DDTHH:MM:SSZ")

    data = generate_voltage_data(1000)
    filtered_data = [record for record in data if
                     start_dt <= datetime.strptime(record.timestamp, '%Y-%m-%dT%H:%M:%SZ') <= end_dt]

    return VoltageResponse(data=filtered_data)


@app.get("/voltage/alerts", response_model=List[VoltageAlert])
def get_voltage_alerts():
    data = generate_voltage_data(1000)
    alerts = []
    for record in data:
        if record.status == "Fault":
            alert_message = f"Voltage anomaly detected: {record.voltage}V at {record.timestamp}. {record.status_message}"
            alerts.append(VoltageAlert(timestamp=record.timestamp, voltage=record.voltage, status=record.status,
                                       alert_message=alert_message))
    return alerts


@app.get("/vehicle/types", response_model=List[VehicleTypeData])
def get_vehicle_types():
    data = generate_vehicle_type_data()
    return data


@app.get("/vehicle/specs", response_model=List[VehicleSpecs])
def get_vehicle_specs():
    data = generate_vehicle_specs()
    return data


@app.post("/voltage/threshold", response_model=VoltageThreshold)
def set_voltage_threshold(threshold: VoltageThreshold):
    global voltage_threshold
    voltage_threshold = threshold
    return voltage_threshold


# Run FastAPI app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
