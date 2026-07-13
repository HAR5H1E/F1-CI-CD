from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import uvicorn
import joblib

app = FastAPI()
app.mount("/static",StaticFiles(directory="App/static"),name="static")

class PredictionResponse(BaseModel):
    Abbreviation : str
    TeamName:str
    CountryEvent: str
    GridPosition:int
    GapPole:float
    GapLeaderFP:float

model = joblib.load("JoblibFiles/F1Modelv1.pkl")
encoder = joblib.load("JoblibFiles/F1Encoder.pkl")
features = joblib.load("JoblibFiles/F1Columns.pkl")


@app.get("/health")
def getHealth():
    return {"Status": "Ok"}

@app.get("/",response_class=HTMLResponse)
def home():
    with open("App/templates/index.html") as file:
        return file.read()

@app.post("/Predict")
def predict(RaceInput : PredictionResponse):
    DataSet = pd.DataFrame([{
        "Abbreviation":RaceInput.Abbreviation,
        "TeamName":RaceInput.TeamName,
        "CountryEvent":RaceInput.CountryEvent,
        "GridPosition":RaceInput.GridPosition,
        "GapPole":RaceInput.GapPole,
        "GapLeaderFP":RaceInput.GapLeaderFP
    }])

    EncodedVal = pd.DataFrame(encoder.transform(DataSet[["Abbreviation","TeamName","CountryEvent"]]),
                       columns=encoder.get_feature_names_out(['Abbreviation', 'TeamName', 'CountryEvent']))
    
    finalInput = pd.concat([DataSet[["GridPosition","GapPole","GapLeaderFP"]].reset_index(drop=True),EncodedVal],
                           axis=1)
    
    finalInput = finalInput.reindex(columns = features,fill_value=0)
    finalVal = model.predict(finalInput)[0]

    return {"Final":round(float(finalVal),2),
            "Final_Position_Rounded": max(1,min(20,round(float(finalVal))))}

  


if  __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port= 8080)
