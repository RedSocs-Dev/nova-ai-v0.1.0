# Sécurité — état actuel et exigences avant déploiement

Mesures présentes : validation Pydantic, limites de taille des messages et documents, liste blanche d'extensions, décodage UTF-8 strict, requêtes SQL paramétrées, clé d'API lue depuis l'environnement, journaux sans contenu de conversation, erreurs fournisseur réduites, CORS configurable, recommandation d'écoute sur localhost.

Risques et travaux requis :
1. Aucun mécanisme d'authentification/autorisation ; ne pas exposer publiquement.
2. Pas de limitation de débit persistante ni de quotas par utilisateur.
3. Le filtrage par extension ne remplace pas l'analyse antivirus ; n'importez que des fichiers de confiance.
4. Les documents peuvent contenir des instructions hostiles ; leur contenu est encadré comme donnée non fiable, mais cela ne garantit pas l'absence d'injection.
5. Pas de sandbox d'exécution de code — aucun code utilisateur n'est exécuté.
6. Ajoutez HTTPS, gestion de secrets dédiée, mises à jour de dépendances, sauvegardes chiffrées et tests de sécurité avant usage sensible.
7. Les routes de mémoire et de documents ne sont pas cloisonnées entre utilisateurs : usage local individuel uniquement.
8. Ne mettez pas `NOVA_API_KEY` dans les journaux, captures d'écran ou dépôts.

Cette version n'est pas certifiée pour un usage en production ou multi-utilisateur.
