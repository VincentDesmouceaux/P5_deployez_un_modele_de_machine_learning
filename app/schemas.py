from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Department = Literal[
    "sales",
    "accounting",
    "hr",
    "technical",
    "support",
    "management",
    "IT",
    "product_mng",
    "marketing",
    "RandD",
]

SalaryLevel = Literal["low", "medium", "high"]


class PredictionInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "satisfaction_level": 0.38,
                "last_evaluation": 0.86,
                "number_project": 6,
                "average_monthly_hours": 260,
                "time_spend_company": 4,
                "work_accident": False,
                "promotion_last_5years": False,
                "department": "technical",
                "salary": "low",
            }
        }
    )

    satisfaction_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Niveau de satisfaction du collaborateur, entre 0 et 1.",
    )
    last_evaluation: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Dernière évaluation du collaborateur, entre 0 et 1.",
    )
    number_project: int = Field(
        ...,
        ge=1,
        le=10,
        description="Nombre de projets attribués au collaborateur.",
    )
    average_monthly_hours: int = Field(
        ...,
        ge=50,
        le=350,
        description="Nombre moyen d'heures travaillées par mois.",
    )
    time_spend_company: int = Field(
        ...,
        ge=0,
        le=20,
        description="Ancienneté dans l'entreprise, en années.",
    )
    work_accident: bool = Field(
        ...,
        description="Indique si le collaborateur a eu un accident du travail.",
    )
    promotion_last_5years: bool = Field(
        ...,
        description="Indique si le collaborateur a eu une promotion dans les cinq dernières années.",
    )
    department: Department = Field(
        ...,
        description="Département du collaborateur.",
    )
    salary: SalaryLevel = Field(
        ...,
        description="Niveau de salaire du collaborateur.",
    )


class PredictionOutput(BaseModel):
    prediction: int = Field(
        ...,
        ge=0,
        le=1,
        description="Classe prédite. 0 = reste, 1 = départ probable.",
    )
    prediction_label: Literal["stay", "leave"] = Field(
        ...,
        description="Libellé métier de la prédiction.",
    )
    probability_leave: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probabilité estimée de départ.",
    )
    model_name: str = Field(
        ...,
        description="Nom du modèle utilisé.",
    )
    model_version: str = Field(
        ...,
        description="Version du modèle utilisé.",
    )


class ModelInfo(BaseModel):
    model_name: str
    model_version: str
    model_type: str
    target: str
    description: str
    input_features: list[str]
