# F1 Race Position Predictor

An ML-powered REST API that predicts a driver's finishing position in a Formula 1 race using pre-race data — grid position, qualifying gap, and practice pace — pulled via the [FastF1](https://github.com/theOehrly/Fast-F1) API. Built as an end-to-end project covering data engineering, model comparison, and API deployment, with a full CI/CD pipeline to AWS. The ML model and the pipeline are equally important deliverables here — this isn't just a notebook, it's meant to ship.

## Live demo

*Coming soon — deployment in progress.*

## How it works

1. **Data pipeline** pulls race, qualifying, and practice session data from FastF1 across the 2023–2025 seasons and builds one training row per driver per race.
2. **Model** (Random Forest) is trained to predict finishing position from pre-race signals only — no information that wouldn't be available before lights out.
3. **API** (FastAPI) serves predictions, with a minimal HTML frontend for quick testing.
4. **Pipeline** containerizes the API with Docker and ships it via GitHub Actions to AWS.

## Results

Evaluated by Mean Absolute Error (MAE), trained on 2023–2024 seasons, tested on 2025:

| Model | MAE | vs. Baseline |
|---|---|---|
| Baseline (grid position = finish position) | 2.72 | — |
| **Random Forest (tuned)** | **2.39** | **~12% better** ✅ |
| CatBoost | 2.50 | ~8% better |
| LightGBM | 2.77 | no improvement |

Random Forest was selected as the production model. Note: the model predicts *expected* finishing position under normal race conditions — it does not and cannot predict incidents like crashes or mechanical failures, which are excluded from training by design.

## Tech stack

- **Data:** FastF1, Pandas
- **ML:** scikit-learn (Random Forest), LightGBM, CatBoost, joblib
- **API:** FastAPI, Pydantic, Uvicorn
- **Frontend:** static HTML + Tailwind CSS (CDN)
- **CI/CD:** Docker, GitHub Actions, AWS (ECR + EC2/ECS Fargate)

## Project structure

```
F1-CI-CD/
├── .github/workflows/   # CI/CD pipeline definitions
├── App/                 # FastAPI app + frontend
├── FinalDataset/        # Processed training/eval data
├── JoblibFiles/         # Serialized preprocessing artifacts
├── Model/               # Trained model files
├── Dockerfile           # Container build for the API
└── README.md
```

## Getting started

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized run)

### Run locally

```bash
git clone https://github.com/HAR5H1E/F1-CI-CD.git
cd F1-CI-CD

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn App.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

> Adjust the module path (`App.main:app`) if your entry point differs.

### Run with Docker

```bash
docker build -t f1-ci-cd .
docker run -p 8000:8000 f1-ci-cd
```

## CI/CD pipeline

Pushes to `main` trigger a GitHub Actions workflow that:

1. Runs tests / linting (if configured)
2. Builds the Docker image
3. Pushes the image to AWS ECR
4. Deploys the updated container to AWS (EC2/ECS Fargate)

See [`.github/workflows`](.github/workflows) for the current pipeline definitions.

## Status

In active development — CI/CD deployment to AWS in progress.