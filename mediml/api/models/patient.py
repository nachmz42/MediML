

from mediml.api.models.patient_dto import PatientDto


class Patient():
    def __init__(self, patient_data: PatientDto):
        self.gender = patient_data.gender.value
        self.age = patient_data.age
        self.hypertension = 1 if patient_data.hypertension else 0
        self.heart_disease = 1 if patient_data.heart_disease else 0
        self.ever_married = "Yes" if patient_data.ever_married else "No"
        self.work_type = patient_data.work_type.value
        self.residence_type = patient_data.residence_type.value
        self.avg_glucose_level = patient_data.avg_glucose_level
        self.bmi = patient_data.bmi
        self.smoking_status = patient_data.smoking_status.value
