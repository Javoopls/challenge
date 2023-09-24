import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from . import model
from model import DelayModel


app = FastAPI()

# Define una clase Pydantic para recibir los datos de entrada en la solicitud POST
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
        # Crea una instancia del modelo
        model = DelayModel()

        # Preprocesa los datos para la predicción
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

        # Realiza la predicción utilizando el modelo
        predictions = model.predict(features)

        # Devuelve la predicción como resultado
        return {"prediction": predictions[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))