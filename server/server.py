from fastapi import FastAPI
from pydantic import BaseModel
from server.features import cleaned_df_from_string 

class ClaimData(BaseModel):
    data: str

app = FastAPI()

@app.post("/score")
def score_claim(claim: ClaimData):
    a = cleaned_df_from_string(claim.data)
    print(a)
    return a.tolist()
