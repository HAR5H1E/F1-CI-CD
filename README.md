# F1 Race Position Predictor
 
An ML-powered API that predicts a driver's finishing position in a Formula 1 race using pre-race data — grid position, qualifying gap, and practice pace — pulled via the [FastF1](https://github.com/theOehrly/Fast-F1) API. Built as an end-to-end project covering data engineering, model comparison, and API deployment, with CI/CD to AWS in progress.
 
## Live demo
_Coming soon — deployment in progress._
 
## How it works
 
1. **Data pipeline** pulls race, qualifying, and practice session data from FastF1 across the 2023–2025 seasons and builds one training row per driver per race.
2. **Model** (Random Forest) is trained to predict finishing position from pre-race signals only — no information that wouldn't be available before lights out.
3. **API** (FastAPI) serves predictions, with a minimal HTML/Tailwind frontend for quick testing.
## Results
 
Evaluated by Mean Absolute Error (MAE), trained on 2023–2024 seasons, tested on 2025:
 
| Model | MAE | vs. Baseline |
|---|---|---|
| Baseline (grid position = finish position) | 2.72 | — |
| **Random Forest (tuned)** | **2.39** | **~12% better** ✅ |
| CatBoost | 2.50 | ~8% better |
| LightGBM | 2.77 | no improvement |
 
Random Forest was selected as the production model. It's worth noting the model predicts *expected* finishing position under normal race conditions — it does not and cannot predict incidents like crashes or mechanical failures, which are excluded from training by design (see [Design Decisions](#design-decisions)).
 
## Tech stack
 
- **Data:** FastF1, Pandas
- **ML:** scikit-learn (Random Forest), LightGBM, CatBoost, joblib
- **API:** FastAPI, Pydantic, Uvicorn
- **Frontend:** static HTML + Tailwind CSS (CDN)
- **Planned:** Docker, GitHub Actions, AWS (ECR + EC2/ECS Fargate)
