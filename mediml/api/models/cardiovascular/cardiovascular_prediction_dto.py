from enum import Enum

from pydantic import BaseModel


class CardiovascularPrediction(str, Enum):
    cardiovascular = "cardiovascular"
    no_cardiovascular = "no_cardiovascular"


class CardiovascularPredictionsDto(BaseModel):
    predictions: list[CardiovascularPrediction]


cardiovascular_prediction = {
    0: CardiovascularPrediction.no_cardiovascular,
    1: CardiovascularPrediction.cardiovascular
}
