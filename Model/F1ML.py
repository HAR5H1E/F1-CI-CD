import joblib
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

FinalSet = pd.read_parquet("./FinalDataset/FinalSet.parquet")


encoder = OneHotEncoder(sparse_output=False,handle_unknown='ignore')

trainVal = FinalSet[FinalSet['Year'].isin([2023,2024])]
testVal  = FinalSet[FinalSet['Year'].isin([2025])]

encoder.fit(trainVal[["Abbreviation","TeamName","CountryEvent"]])

trainDF = pd.DataFrame(encoder.transform(trainVal[["Abbreviation","TeamName","CountryEvent"]]),
                       columns=encoder.get_feature_names_out(['Abbreviation', 'TeamName', 'CountryEvent']))

testDF = pd.DataFrame(encoder.transform(testVal[["Abbreviation","TeamName","CountryEvent"]]),
                       columns=encoder.get_feature_names_out(['Abbreviation', 'TeamName', 'CountryEvent']))

X_Train = pd.concat([trainVal[["GridPosition","GapPole","GapLeaderFP"]].reset_index(drop=True),
                     trainDF],
                     axis=1)
X_Test = pd.concat([testVal[["GridPosition","GapPole","GapLeaderFP"]].reset_index(drop=True),
                     testDF],
                     axis=1)

Y_Train = trainVal["ClassifiedPosition"].reset_index(drop=True)
Y_Test  = testVal["ClassifiedPosition"].reset_index(drop=True)

featureCols = X_Train.columns.to_list()

rf = RandomForestRegressor(n_estimators=200,max_depth=5, random_state=42)
rf.fit(X_Train, Y_Train)
print("RF MAE:", mean_absolute_error(Y_Test, rf.predict(X_Test)))

"""
lgbm = lgb.LGBMRegressor(n_estimators=300, random_state=42,num_leaves=15,min_child_samples=10)
lgbm.fit(X_Train, Y_Train)
print("LGBM MAE:", mean_absolute_error(Y_Test, lgbm.predict(X_Test)))

cb = CatBoostRegressor(iterations=300, random_state=42, verbose=False)
cb.fit(X_Train, Y_Train)
print("CatBoost MAE:", mean_absolute_error(Y_Test, cb.predict(X_Test)))
"""
baseline_mae = mean_absolute_error(Y_Test, X_Test['GridPosition'])
print("Baseline MAE (grid = finish):", baseline_mae)

SerialModel = Path("./JoblibFiles")
SerialModel.mkdir(parents=True,exist_ok=True)

joblib.dump(rf,"./JoblibFiles/F1Modelv1.pkl")
joblib.dump(encoder,"./JoblibFiles/F1Encoder.pkl")
joblib.dump(featureCols,"./JoblibFiles/F1Columns.pkl")
