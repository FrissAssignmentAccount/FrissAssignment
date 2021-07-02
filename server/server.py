import os
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import sklearn

from server.features import cleaned_features_from_string


MODEL_FILENAME = "model.pickle"
MODEL_PATH = os.path.join(os.path.dirname(__file__), MODEL_FILENAME)


def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


class ClaimData(BaseModel):
    data: str


model = load_model()
app = FastAPI()


@app.post("/score")
def score_claim(claim: ClaimData):
    cleaned_features = cleaned_features_from_string(claim.data)
    prediction = model.predict(cleaned_features).tolist()
    return {"fraud": prediction[0]}
