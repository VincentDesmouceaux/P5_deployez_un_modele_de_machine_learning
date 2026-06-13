#!/bin/bash

echo "Ouverture de DBeaver pour visualiser la base PostgreSQL du projet P5..."
echo ""
echo "Connexion attendue :"
echo "- Host     : localhost"
echo "- Port     : 5432"
echo "- Database : p5_ml_api"
echo "- Schema   : ml_api"
echo ""
echo "Vue à afficher dans DBeaver :"
echo "- ml_api.v_prediction_traces"
echo ""
echo "Requête de démonstration :"
echo "- db/sql/07_visualize_prediction_traces.sql"
echo ""

open -a DBeaver db/sql/07_visualize_prediction_traces.sql