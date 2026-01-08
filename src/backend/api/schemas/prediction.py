from pydantic import BaseModel

class PredictionResponse(BaseModel):
    prediction: str
    probabilities: dict