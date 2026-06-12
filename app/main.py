from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.schemas import ModelInfo, PredictionInput, PredictionOutput
from app.services.model_service import get_model_info, predict_attrition

app = FastAPI(
    title="P5 - API de déploiement ML",
    description="API FastAPI pour exposer un modèle de machine learning de prédiction d'attrition.",
    version="0.3.0",
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Monitoring"])
def health_check():
    return {
        "status": "ok",
        "service": "p5-ml-api",
        "version": "0.3.0",
    }


@app.get("/model-info", response_model=ModelInfo, tags=["Model"])
def model_info():
    return get_model_info()


@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
def predict(input_data: PredictionInput):
    return predict_attrition(input_data)
