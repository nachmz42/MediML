from enum import Enum

from pydantic import BaseModel


class StrokePrediction(str, Enum):
    stroke = "stroke"
    no_stroke = "no_stroke"


class StrokePredictionsDto(BaseModel):
    predictions: list[StrokePrediction]


stroke_prediction = {
    0: StrokePrediction.no_stroke,
    1: StrokePrediction.stroke
}
