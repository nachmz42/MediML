from enum import Enum

from pydantic import BaseModel


class GeneralHealth(str, Enum):
    poor = 'Poor'
    fair = 'Fair'
    good = 'Good'
    very_good = 'Very Good'
    excellent = 'Excellent'

class Checkup(str, Enum):
    never = 'Never'
    more_five_years = '5 or more years ago'
    five_years = 'Within the past 5 years'
    two_years = 'Within the past 2 years'
    one_year = 'Within the past year'

class Gender(str, Enum):
    male = "Male"
    female = "Female"

class AgeCategory(str,Enum):
    age_18_24 = '18-24'
    age_25_29 = '25-29'
    age_30_34 = '30-34'
    age_35_39 = '35-39'
    age_40_44 = '40-44'
    age_45_49 = '45-49'
    age_50_54 = '50-54'
    age_55_59 = '55-59'
    age_60_64 = '60-64'
    age_65_69 = '65-69'
    age_70_74 = '70-74'
    age_75_79 = '75-79'
    age_80 = '80+'

class CardiovascularPatientDto(BaseModel):
    general_health: GeneralHealth
    checkup:Checkup
    exercise:bool
    skin_cancer:bool
    other_cancer:bool
    depression:bool
    diabetes:bool
    arthritis:bool
    gender:Gender
    age: AgeCategory
    height: float
    weight: float
    bmi: float
    smoking:bool
    alcohol_consumption: float
    fruit_consumption: float
    green_vegetable_consumption: float
    fried_potato_consumption:float

class CardiovascularPatientsDto(BaseModel):
    patients = list[CardiovascularPatientDto]
