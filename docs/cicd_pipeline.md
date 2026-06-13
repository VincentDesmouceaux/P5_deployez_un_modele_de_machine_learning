# 🔁 Documentation CI/CD — GitHub Actions et déploiement Hugging Face Spaces

## Objectif

Cette documentation décrit le pipeline d’intégration continue et de déploiement continu du projet **P5 — Déployez un modèle de Machine Learning**.

Le pipeline CI/CD permet de :

* vérifier automatiquement la qualité du projet ;
* installer les dépendances Python ;
* exécuter les tests unitaires et fonctionnels ;
* générer un rapport de couverture ;
* publier le rapport de couverture en artifact GitHub Actions ;
* déployer automatiquement l’API sur Hugging Face Spaces depuis la branche `main`.

L’objectif est de garantir qu’une version livrée sur `main` est testée, documentée et déployable.

---

## 1. Workflow principal

Le workflow GitHub Actions principal est défini dans le fichier :

```text
.github/workflows/ci-cd.yml
```

Ce fichier décrit les étapes automatisées exécutées par GitHub Actions.

---

## 2. Branches surveillées

Le pipeline se déclenche sur les branches suivantes :

```text
main
develop
feature/**
```

Il se déclenche également lors des pull requests vers :

```text
main
develop
```

Cette organisation permet de tester le code à plusieurs niveaux :

| Branche      | Rôle                                     |
| ------------ | ---------------------------------------- |
| `feature/**` | Développement d’une fonctionnalité       |
| `develop`    | Intégration des fonctionnalités validées |
| `main`       | Version stable et déployable             |

---

## 3. Environnements Git

### Développement

Les branches `feature/**` servent à développer une fonctionnalité isolée.

Exemples :

```text
feature/fastapi-api
feature/model-loading
feature/unit-functional-tests
feature/documentation
```

Les tests peuvent être lancés automatiquement à chaque push sur une branche de feature.

### Intégration

La branche `develop` sert à regrouper les fonctionnalités terminées.

Elle permet de vérifier que plusieurs développements fonctionnent ensemble avant passage sur `main`.

### Production

La branche `main` représente la version stable du projet.

Le déploiement vers Hugging Face Spaces est exécuté uniquement depuis `main`, après réussite des tests.

---

## 4. Étapes du pipeline

Le pipeline suit ce flux :

```text
Checkout repository
        ↓
Setup Python 3.11
        ↓
Install dependencies
        ↓
Run tests with coverage
        ↓
Generate coverage reports
        ↓
Upload coverage artifact
        ↓
Deploy to Hugging Face Spaces
```

---

## 5. Job de test

Le job de test vérifie que le projet fonctionne correctement avant tout déploiement.

Il réalise les actions suivantes :

1. récupération du repository ;
2. installation de Python 3.11 ;
3. installation des dépendances ;
4. exécution de la suite de tests ;
5. génération du rapport de couverture ;
6. publication du rapport en artifact.

Commande principale utilisée :

```bash
python -m pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=xml:reports/coverage.xml \
  --cov-report=html:reports/coverage_html
```

---

## 6. Tests exécutés

La suite de tests couvre :

* les endpoints FastAPI ;
* les schémas Pydantic ;
* le service de chargement du modèle ;
* le service de prédiction ;
* le service de traçabilité PostgreSQL ;
* le parcours fonctionnel complet de l’API.

Fichiers de tests principaux :

| Fichier                                | Rôle                                 |
| -------------------------------------- | ------------------------------------ |
| `tests/test_health.py`                 | Test de l’endpoint `/health`         |
| `tests/test_prediction.py`             | Tests de `/model-info` et `/predict` |
| `tests/test_schemas.py`                | Tests unitaires des schémas Pydantic |
| `tests/test_model_service.py`          | Tests du service modèle              |
| `tests/test_prediction_log_service.py` | Tests du service de traçabilité      |
| `tests/test_functional_api.py`         | Tests fonctionnels API complets      |

Résultat validé localement :

```text
24 passed
coverage 98%
```

---

## 7. Rapport de couverture

Le pipeline génère deux formats de rapport de couverture :

```text
reports/coverage.xml
reports/coverage_html/
```

Le rapport XML est utile pour les outils automatisés.

Le rapport HTML permet de consulter visuellement :

* les fichiers couverts ;
* les lignes exécutées ;
* les lignes non couvertes ;
* le taux global de couverture.

Commande locale équivalente :

```bash
python -m pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=xml:reports/coverage.xml \
  --cov-report=html:reports/coverage_html
```

Pour ouvrir le rapport HTML localement :

```bash
open reports/coverage_html/index.html
```

---

## 8. Artifact GitHub Actions

Le pipeline publie le rapport de couverture sous forme d’artifact GitHub Actions.

Nom de l’artifact :

```text
coverage-report
```

Contenu attendu :

```text
reports/coverage.xml
reports/coverage_html/
```

Cela permet de télécharger le rapport de couverture depuis l’interface GitHub Actions après l’exécution du workflow.

---

## 9. Job de déploiement

Le job de déploiement synchronise le repository avec Hugging Face Spaces.

Il est exécuté uniquement si :

* les tests passent ;
* la branche courante est `main`.

Cette règle évite de déployer automatiquement une branche de développement ou une branche d’intégration.

---

## 10. Déploiement Hugging Face Spaces

L’application est déployée sur Hugging Face Spaces avec le SDK Docker.

Space utilisé :

```text
TheCruiser/p5-ml-api-futurisys
```

URL publique :

```text
https://thecruiser-p5-ml-api-futurisys.hf.space
```

Swagger en ligne :

```text
https://thecruiser-p5-ml-api-futurisys.hf.space/docs
```

---

## 11. Configuration Hugging Face

La configuration du Space est définie dans le bloc YAML du README :

```yaml
---
title: P5 ML API Futurisys
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---
```

Le champ :

```yaml
app_port: 7860
```

indique à Hugging Face Spaces le port interne utilisé par l’application Docker.

Ce port n’est pas un secret. Il sert uniquement au routage de l’application dans l’environnement Hugging Face.

---

## 12. Secrets et variables GitHub

Le déploiement utilise un secret GitHub :

```text
HF_TOKEN
```

Ce secret contient le token Hugging Face utilisé pour pousser le projet vers le Space.

Il ne doit jamais être écrit dans le code, dans le README ou dans un fichier versionné.

Le pipeline peut également utiliser une variable :

```text
HF_SPACE_ID
```

Valeur attendue :

```text
TheCruiser/p5-ml-api-futurisys
```

---

## 13. Sécurité CI/CD

Points de vigilance :

* ne jamais versionner `HF_TOKEN` ;
* ne jamais afficher le token dans les logs ;
* ne jamais stocker de mot de passe dans le repository ;
* limiter le déploiement automatique à la branche `main` ;
* vérifier que les tests passent avant déploiement ;
* vérifier que le fichier `.env` reste ignoré par Git ;
* vérifier que les rapports générés localement ne sont pas commités.

---

## 14. Commandes locales équivalentes

### Vérifier la branche courante

```bash
git branch --show-current
```

### Vérifier l’état Git

```bash
git status
```

### Lancer les tests

```bash
python -m pytest
```

### Lancer les tests avec couverture

```bash
python -m pytest --cov=app --cov-report=term-missing
```

### Générer les rapports HTML et XML

```bash
python -m pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=xml:reports/coverage.xml \
  --cov-report=html:reports/coverage_html
```

### Ouvrir le rapport HTML

```bash
open reports/coverage_html/index.html
```

### Pousser sur `main`

```bash
git push origin main
```

---

## 15. Validation avant livraison

Avant de livrer une nouvelle version, vérifier :

* que la branche est `main` ;
* que le working tree est propre ;
* que les tests passent ;
* que la couverture est satisfaisante ;
* que la documentation est à jour ;
* que les secrets ne sont pas versionnés ;
* que le déploiement Hugging Face fonctionne ;
* que Swagger est accessible.

Commandes de vérification :

```bash
git branch --show-current
git status
python -m pytest --cov=app --cov-report=term-missing
curl https://thecruiser-p5-ml-api-futurisys.hf.space/health
```

---

## 16. Versioning

Les versions du projet sont suivies avec des tags Git.

Exemple :

```bash
git tag -a v0.7.0 -m "Documentation complète du modèle, de l API et de la maintenance"
git push origin v0.7.0
```

Les tags permettent d’identifier précisément les étapes majeures du projet :

| Version  | Rôle                                        |
| -------- | ------------------------------------------- |
| `v0.5.6` | Visualisation PostgreSQL                    |
| `v0.6.0` | Tests unitaires, fonctionnels et couverture |
| `v0.7.0` | Documentation complète                      |

---

## 17. Résumé

Le pipeline CI/CD garantit que le projet est testé et validé avant déploiement.

Il assure :

```text
Code GitHub
→ Installation Python
→ Tests Pytest
→ Couverture
→ Artifact coverage-report
→ Déploiement Hugging Face Spaces
```

Cette automatisation renforce la fiabilité du projet et facilite la maintenance des futures versions.
