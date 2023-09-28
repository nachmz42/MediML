from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mediml.api.models.cardiovascular.cardiovascular_patient_dto import CardiovascularPatientsDto
from mediml.api.models.cardiovascular.cardiovascular_prediction_dto import CardiovascularPredictionsDto

from mediml.api.models.stroke.patient_dto import PatientsDto
from mediml.api.models.stroke.stroke_prediction_dto import StrokePredictionsDto
from mediml.api.services.cardiovascular.adapters import intPredictionsToCardiovascularPredictions, patientsDtoToCardiovascularPatientsDataFrame
from mediml.api.services.stroke.adapters import (intPredictionsToStrokePredictions,
                                          patientsDtoToPatientsDataFrame)
from mediml.ml_logic.cardiovascular.registry import load_pipeline as load_cardiovascular_pipeline
from mediml.ml_logic.stroke.registry import load_pipeline as load_stroke_pipeline


app = FastAPI()

# 💡 Preload the pipeline to accelerate the predictions
# We want to avoid loading the heavy Deep Learning pipeline from MLflow at each `get("/predict")`
# The trick is to load the pipeline in memory when the Uvicorn server starts
# and then store the pipeline in an `app.state.pipeline` global variable, accessible across all routes!
# This will prove very useful for the Demo Day
app.state.pipeline_stroke = load_stroke_pipeline()
app.state.pipeline_cardiovascular = load_cardiovascular_pipeline()



# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/')
def index() -> dict:
    return {'ok': True}


@app.post('/predict/stroke')
async def predictStroke(patient_dto: PatientsDto) -> StrokePredictionsDto:
    X_pred = patientsDtoToPatientsDataFrame(patient_dto)

    pipeline = app.state.pipeline_stroke
    assert pipeline is not None

    y_pred = pipeline.predict(X_pred)

    predictions = intPredictionsToStrokePredictions(y_pred)

    return StrokePredictionsDto(predictions=predictions)


@app.post('/predict/cardiovascular')
async def predictCardiovascular(patient_dto: CardiovascularPatientsDto) -> CardiovascularPredictionsDto:
    X_pred = patientsDtoToCardiovascularPatientsDataFrame(patient_dto)

    pipeline = app.state.pipeline_cardiovascular
    assert pipeline is not None

    y_pred = pipeline.predict(X_pred)

    predictions = intPredictionsToCardiovascularPredictions(y_pred)

    return CardiovascularPredictionsDto(predictions=predictions)
