import pandas as pd

from mediml.api.models.patient import Patient
from mediml.api.models.patient_dto import PatientDto, PatientsDto
from mediml.api.models.stroke_prediction_dto import (StrokePrediction,
                                                     stroke_prediction)
from mediml.environment.params import COLUMN_NAMES_RAW


def patientsDtoToPatientsDataFrame(patient_dtos: PatientsDto) -> pd.DataFrame:
    """
    Converts a list of PatientsDto to a Pandas DataFrame
    """
    return pd.DataFrame([patientDtoToPatientDataFrame(patient_dto) for patient_dto in patient_dtos.patients],
                        columns=COLUMN_NAMES_RAW)


def patientDtoToPatientDataFrame(patient_dto: PatientDto) -> list:
    """
    Converts a PatientDto to a Patient
    """
    return list(Patient(patient_dto).__dict__.values())


def intPredictionsToStrokePredictions(y_pred: list[int]) -> list[StrokePrediction]:
    """
    Converts a list of int predictions to a list of stroke predictions
    """
    return list(map(lambda pred: stroke_prediction[pred], y_pred))
