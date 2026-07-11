from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class PredictionResponse():
    Abbreviation : str
    TeamName:str
    CountryEvent: str
    GridPosition:int
    GapPole:float
    GapLeaderFP:float

@app.get("/health")
def getHealth():
    return {"Status": "Ok"}

@app.get("/Predict")
def predict(RaceInput : PredictionResponse):
    return {"Status":"Ok"}


if  __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port= 8080)
