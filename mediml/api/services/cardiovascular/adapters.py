import pandas as pd



from mediml.api.models.cardiovascular.cardiovascular_patient import CardiovascularPatient
from mediml.api.models.cardiovascular.cardiovascular_patient_dto import CardiovascularPatientDto, CardiovascularPatientsDto
from mediml.api.models.cardiovascular.cardiovascular_prediction_dto import CardiovascularPrediction, cardiovascular_prediction
from mediml.environment.params import COLUMN_NAMES_CARDIOVASCULAR_RAW

def patientsDtoToCardiovascularPatientsDataFrame(patient_dtos: CardiovascularPatientsDto) -> pd.DataFrame:
    """
    Converts a list of PatientsDto to a Pandas DataFrame
    """
    return pd.DataFrame([cardiovascularPatientDtoToPatientDataFrame(patient_dto) for patient_dto in patient_dtos.patients],
                        columns=COLUMN_NAMES_CARDIOVASCULAR_RAW)


def cardiovascularPatientDtoToPatientDataFrame(patient_dto: CardiovascularPatientDto) -> list:
    """
    Converts a CardiovascularPatientDto to a CardiovascularPatient
    """
    return list(CardiovascularPatient(patient_dto).__dict__.values())


def intPredictionsToCardiovascularPredictions(y_pred: list[int]) -> list[CardiovascularPrediction]:
    """
    Converts a list of int predictions to a list of cardiovascular predictions
    """
    return list(map(lambda pred: cardiovascular_prediction[pred], y_pred))
