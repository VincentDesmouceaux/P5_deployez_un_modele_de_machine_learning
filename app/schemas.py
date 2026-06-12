from pydantic import BaseModel, ConfigDict, Field


class PredictionInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 41,
                "genre": "F",
                "revenu_mensuel": 5993,
                "statut_marital": "Célibataire",
                "departement": "Commercial",
                "poste": "Cadre Commercial",
                "nombre_experiences_precedentes": 8,
                "nombre_heures_travailless": 80,
                "annee_experience_totale": 8,
                "annees_dans_l_entreprise": 6,
                "annees_dans_le_poste_actuel": 4,
                "satisfaction_employee_environnement": 2,
                "note_evaluation_precedente": 3,
                "niveau_hierarchique_poste": 2,
                "satisfaction_employee_nature_travail": 4,
                "satisfaction_employee_equipe": 1,
                "satisfaction_employee_equilibre_pro_perso": 1,
                "note_evaluation_actuelle": 3,
                "heure_supplementaires": "Oui",
                "augementation_salaire_precedente": 11,
                "nombre_participation_pee": 0,
                "nb_formations_suivies": 0,
                "nombre_employee_sous_responsabilite": 0,
                "distance_domicile_travail": 1,
                "niveau_education": 2,
                "domaine_etude": "Sciences de la Vie",
                "ayant_enfants": "Y",
                "frequence_deplacement": "Occasionnel",
                "annees_depuis_la_derniere_promotion": 0,
                "annes_sous_responsable_actuel": 5
            }
        }
    )

    age: int = Field(..., ge=18, le=70)
    genre: str = Field(...)
    revenu_mensuel: int = Field(..., ge=0)
    statut_marital: str = Field(...)
    departement: str = Field(...)
    poste: str = Field(...)
    nombre_experiences_precedentes: int = Field(..., ge=0)
    nombre_heures_travailless: int = Field(..., ge=0)
    annee_experience_totale: int = Field(..., ge=0)
    annees_dans_l_entreprise: int = Field(..., ge=0)
    annees_dans_le_poste_actuel: int = Field(..., ge=0)
    satisfaction_employee_environnement: int = Field(..., ge=1, le=4)
    note_evaluation_precedente: int = Field(..., ge=1, le=5)
    niveau_hierarchique_poste: int = Field(..., ge=1)
    satisfaction_employee_nature_travail: int = Field(..., ge=1, le=4)
    satisfaction_employee_equipe: int = Field(..., ge=1, le=4)
    satisfaction_employee_equilibre_pro_perso: int = Field(..., ge=1, le=4)
    note_evaluation_actuelle: int = Field(..., ge=1, le=5)
    heure_supplementaires: str = Field(...)
    augementation_salaire_precedente: int = Field(..., ge=0, le=100)
    nombre_participation_pee: int = Field(..., ge=0)
    nb_formations_suivies: int = Field(..., ge=0)
    nombre_employee_sous_responsabilite: int = Field(..., ge=0)
    distance_domicile_travail: int = Field(..., ge=0)
    niveau_education: int = Field(..., ge=1, le=5)
    domaine_etude: str = Field(...)
    ayant_enfants: str = Field(...)
    frequence_deplacement: str = Field(...)
    annees_depuis_la_derniere_promotion: int = Field(..., ge=0)
    annes_sous_responsable_actuel: int = Field(..., ge=0)


class PredictionOutput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prediction": 1,
                "prediction_label": "leave",
                "probability_leave": 0.7825,
                "model_name": "attrition-random-forest",
                "model_version": "0.5.0"
            }
        }
    )

    prediction: int = Field(..., ge=0, le=1)
    prediction_label: str = Field(...)
    probability_leave: float = Field(..., ge=0.0, le=1.0)
    model_name: str = Field(...)
    model_version: str = Field(...)


class ModelInfo(BaseModel):
    model_name: str
    model_version: str
    model_type: str
    target: str
    description: str
    input_features: list[str]
