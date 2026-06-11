from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="P5 - API de déploiement ML",
    description="API FastAPI pour exposer le modèle de machine learning du projet 4.",
    version="0.2.0",
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Monitoring"])
def health_check():
    return {
        "status": "ok",
        "service": "p5-ml-api",
        "version": "0.2.0",
    }
