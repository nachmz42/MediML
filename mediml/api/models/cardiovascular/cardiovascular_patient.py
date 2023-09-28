
from mediml.api.models.cardiovascular.cardiovascular_patient_dto import CardiovascularPatientDto


class CardiovascularPatient():
    def __init__(self, patient_data: CardiovascularPatientDto):
        self.general_health = patient_data.general_health
        self.checkup = patient_data.checkup
        self.exercise = "Yes" if patient_data.exercise else "No"
        self.skin_cancer = "Yes" if patient_data.skin_cancer else "No"
        self.other_cancer = "Yes" if patient_data.other_cancer else "No"
        self.depression = "Yes" if patient_data.depression else "No"
        self.diabetes = "Yes" if patient_data.diabetes else "No"
        self.arthritis = "Yes" if patient_data.arthritis else "No"
        self.gender = patient_data.gender
        self.age = patient_data.age
        self.height = patient_data.height
        self.weight = patient_data.weight
        self.bmi = patient_data.bmi
        self.smoking = "Yes" if patient_data.smoking else "No"
        self.alcohol_consumption = patient_data.alcohol_consumption
        self.fruit_consumption = patient_data.fruit_consumption
        self.green_vegetable_consumption = patient_data.green_vegetable_consumption
        self.fried_potato_consumption = patient_data.fried_potato_consumption
