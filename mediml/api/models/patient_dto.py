from enum import Enum

from pydantic import BaseModel


class WorkType(str, Enum):
    children = "children"
    govt_jov = "Govt_jov"
    never_worked = "Never_worked"


class ResidenceType(str, Enum):
    rural = "Rural"
    urban = "Urban"


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class SmokingStatus(str, Enum):
    formerly_smoked = "formerly smoked"
    never_smoked = "never smoked"
    smokes = "smokes"
    unknown = "Unknown"


class PatientDto(BaseModel):
    gender: Gender
    age: int
    hypertension: bool
    heart_disease: bool
    ever_married: bool
    work_type: WorkType
    residence_type: ResidenceType
    avg_glucose_level: float
    bmi: float
    smoking_status: SmokingStatus


class PatientsDto(BaseModel):
    patients: list[PatientDto]
