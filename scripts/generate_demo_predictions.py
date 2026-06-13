import json
import os
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

API_URL = "http://127.0.0.1:8000/predict"
DEFAULT_LIMIT = int(os.getenv("DEMO_LIMIT", "20"))

df = pd.read_csv("data/employee_attrition.csv")


def clean_percent(value):
    if pd.isna(value):
        return 0
    return int(str(value).replace("%", "").replace(" ", "").replace(",", ".").strip())


def clean_int(value, default=0):
    if pd.isna(value):
        return default
    return int(float(str(value).replace(",", ".").strip()))


def clean_str(value, default="Inconnu"):
    if pd.isna(value):
        return default
    return str(value).strip()


def build_payload(row):
    return {
        "age": clean_int(row["age"], 35),
        "genre": clean_str(row["genre"]),
        "revenu_mensuel": clean_int(row["revenu_mensuel"], 0),
        "statut_marital": clean_str(row["statut_marital"]),
        "departement": clean_str(row["departement"]),
        "poste": clean_str(row["poste"]),
        "nombre_experiences_precedentes": clean_int(row["nombre_experiences_precedentes"], 0),
        "nombre_heures_travailless": clean_int(row["nombre_heures_travailless"], 0),
        "annee_experience_totale": clean_int(row["annee_experience_totale"], 0),
        "annees_dans_l_entreprise": clean_int(row["annees_dans_l_entreprise"], 0),
        "annees_dans_le_poste_actuel": clean_int(row["annees_dans_le_poste_actuel"], 0),
        "satisfaction_employee_environnement": clean_int(row["satisfaction_employee_environnement"], 2),
        "note_evaluation_precedente": clean_int(row["note_evaluation_precedente"], 3),
        "niveau_hierarchique_poste": clean_int(row["niveau_hierarchique_poste"], 1),
        "satisfaction_employee_nature_travail": clean_int(row["satisfaction_employee_nature_travail"], 2),
        "satisfaction_employee_equipe": clean_int(row["satisfaction_employee_equipe"], 2),
        "satisfaction_employee_equilibre_pro_perso": clean_int(row["satisfaction_employee_equilibre_pro_perso"], 2),
        "note_evaluation_actuelle": clean_int(row["note_evaluation_actuelle"], 3),
        "heure_supplementaires": clean_str(row["heure_supplementaires"]),
        "augementation_salaire_precedente": clean_percent(row["augementation_salaire_precedente"]),
        "nombre_participation_pee": clean_int(row["nombre_participation_pee"], 0),
        "nb_formations_suivies": clean_int(row["nb_formations_suivies"], 0),
        "nombre_employee_sous_responsabilite": clean_int(row["nombre_employee_sous_responsabilite"], 0),
        "distance_domicile_travail": clean_int(row["distance_domicile_travail"], 0),
        "niveau_education": clean_int(row["niveau_education"], 2),
        "domaine_etude": clean_str(row["domaine_etude"]),
        "ayant_enfants": clean_str(row["ayant_enfants"]),
        "frequence_deplacement": clean_str(row["frequence_deplacement"]),
        "annees_depuis_la_derniere_promotion": clean_int(row["annees_depuis_la_derniere_promotion"], 0),
        "annes_sous_responsable_actuel": clean_int(row["annes_sous_responsable_actuel"], 0),
    }


success_count = 0

for index, row in df.head(DEFAULT_LIMIT).iterrows():
    payload = build_payload(row)

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        response = urllib.request.urlopen(request)
        result = json.loads(response.read().decode("utf-8"))
        success_count += 1

        print(
            f"Ligne {index} -> "
            f"prediction={result['prediction']} | "
            f"label={result['prediction_label']} | "
            f"proba={result['probability_leave']}"
        )

    except urllib.error.HTTPError as error:
        print(f"Erreur ligne {index} : HTTP {error.code}")
        print(error.read().decode("utf-8"))

print()
print(f"Nombre de prédictions envoyées avec succès : {success_count}")