import fastf1
import pandas as pd
from fastf1 import Cache
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error

cacheDir = Path("./DataCache")
cacheDir.mkdir(parents=True,exist_ok=True)
Cache.enable_cache(cacheDir)

def PraticeCalc(rounds):
    if rounds["EventFormat"] != "conventional":
        fpSessions = Event.get_practice(1)
        fpSessions.load()
        BestFP = pd.DataFrame(fpSessions.laps)
        BestFP = BestFP.groupby("Driver")["LapTime"].min().reset_index()
        BestTimeFp = BestFP["LapTime"].min()
        BestFP["GapLeaderFP"] = (BestFP["LapTime"] - BestTimeFp)
        BestFP["GapLeaderFP"] = BestFP["GapLeaderFP"].dt.total_seconds()

    else:
        fpSessions = [Event.get_practice(1),
                      Event.get_practice(2),
                      Event.get_practice(3)]
        
        for fp in fpSessions:
            fp.load()
        AllFP = pd.concat([fpSessions[0].laps,fpSessions[1].laps,fpSessions[2].laps],ignore_index=True)

        BestFP = AllFP.groupby("Driver")["LapTime"].min().reset_index()
        BestTimeFp = BestFP["LapTime"].min()
        BestFP["GapLeaderFP"] = (BestFP["LapTime"] - BestTimeFp)
        BestFP["GapLeaderFP"] = BestFP["GapLeaderFP"].dt.total_seconds()

    BestFP = BestFP.sort_values(by="GapLeaderFP",ascending=True).reset_index(drop=True)
    return BestFP

FinalSet = None   
allRaces = []
Years = [2023,2024,2025]
for Year in Years:
    schecule = fastf1.get_event_schedule(Year,include_testing=False)
    for index,rounds in schecule.iterrows():
        Event = schecule.get_event_by_name(rounds["EventName"])
        Race = Event.get_race()
        Quali = Event.get_qualifying()

        Race.load()
        Quali.load()

        RaceResult = Race.results[Race.results["Status"]!="Retired"].copy()
        RaceResult = RaceResult[RaceResult["ClassifiedPosition"].str.isnumeric()].copy()
        RaceResult["ClassifiedPosition"] = RaceResult["ClassifiedPosition"].astype(int)
        RaceResult = pd.DataFrame(RaceResult)

        QualiResult = pd.DataFrame(Quali.results)
        QualiResult["BestQualiTimes"] = QualiResult["Q3"].fillna(QualiResult["Q2"]).fillna(QualiResult["Q1"])

        BestPoleTime = QualiResult["BestQualiTimes"].min()
        QualiResult["GapPole"] = (QualiResult["BestQualiTimes"] - BestPoleTime)
        QualiResult["GapPole"] = QualiResult["GapPole"].dt.total_seconds()
        QualiResult = QualiResult.sort_values(by="GapPole",ascending=True).reset_index(drop=True)

        QualiClean = QualiResult[["Abbreviation","GapPole"]]
        RaceClean = RaceResult[["Abbreviation","TeamName","GridPosition","ClassifiedPosition"]]
        FpClean = PraticeCalc(rounds)
        FpClean = FpClean[["Driver","GapLeaderFP"]]

        RaceRow = RaceClean.merge(QualiClean,on="Abbreviation",how="left")
        RaceRow = RaceRow.merge(FpClean,left_on="Abbreviation",right_on="Driver",how="left")
        RaceRow = RaceRow.dropna(subset=["GapLeaderFP","GridPosition","GapPole","ClassifiedPosition"])
        RaceRow["CountryEvent"] = rounds["EventName"]
        RaceRow["Year"] = Year

        RaceRow=RaceRow.drop(columns=["Driver"])
        allRaces.append(RaceRow)

FinalSet = pd.concat(allRaces,ignore_index=True)
FinalSet = FinalSet.dropna()

FinalDataSet = Path("./FinalDataset")
FinalDataSet.mkdir(parents=True,exist_ok=True)
FinalSet.to_csv("./FinalDataset/FinalSet.csv",index = False)
FinalSet.to_parquet("./FinalDataset/FinalSet.parquet",index = False)