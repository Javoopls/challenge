import pandas as pd
from model import DelayModel
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException


app = FastAPI()

# Defines a Pydantic class to receive the input data in the POST request
class FlightData(BaseModel):
    FechaI: str
    VloI: str
    OriI: str
    DesI: str
    EmpI: str
    FechaO: str
    VloO: str
    OriO: str
    DesO: str
    EmpO: str

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(data: FlightData) -> dict:
    try:
        # Create an instance of the model
        model = DelayModel()

        # Preprocess data for prediction
        input_data = pd.DataFrame([{
            'Fecha-I': data.FechaI,
            'Vlo-I': data.VloI,
            'Ori-I': data.OriI,
            'Des-I': data.DesI,
            'Emp-I': data.EmpI,
            'Fecha-O': data.FechaO,
            'Vlo-O': data.VloO,
            'Ori-O': data.OriO,
            'Des-O': data.DesO,
            'Emp-O': data.EmpO
        }])
        features = model.preprocess(input_data)

        # Make the prediction using the model
        predictions = model.predict(features)

        # Returns the prediction as a result
        return {"prediction": predictions[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))