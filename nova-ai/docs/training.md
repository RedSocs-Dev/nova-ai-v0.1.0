# Évaluation et entraînement

Aucun entraînement n'est exécuté par l'application. Ajouter un document met à jour la base de connaissances, pas les poids du modèle.

Étapes recommandées avant un fine-tuning :
1. Définir des cas d'évaluation français/anglais et des critères mesurables.
2. Versionner les données et leur provenance ; contrôler les droits, doublons et données personnelles.
3. Séparer strictement entraînement, validation et test.
4. Établir une référence avec le modèle existant et enregistrer coût, latence et qualité.
5. Vérifier licence, format et ressources GPU du modèle choisi.
6. Tester PEFT/LoRA sur une petite expérience reproductible.
7. Comparer les résultats, faire valider les changements, puis déployer avec retour arrière.

Un entraînement depuis zéro d'un modèle de pointe n'est pas réaliste sur le matériel CPU modeste observé lors de la construction.
