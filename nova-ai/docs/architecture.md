# Architecture

- `app/config.py` : configuration par variables d'environnement.
- `app/db.py` : schéma SQLite et gestion des transactions.
- `app/providers.py` : interface minimale de génération et de diagnostic pour Ollama et API compatibles OpenAI.
- `app/knowledge.py` : import UTF-8, empreinte SHA-256, recherche lexicale transparente.
- `app/main.py` : API HTTP, validation, historique, mémoire et intégration des composants.
- `app/static/index.html` : interface web autonome sans chaîne de compilation frontend.
- `tests/` : tests API et connecteur.

Le flux de chat charge les 20 derniers messages, recherche des passages locaux, ajoute un message système qui considère les documents comme des données non fiables, appelle le fournisseur configuré, puis persiste la réponse. Les erreurs du fournisseur produisent une réponse HTTP 503. Le socle ne met pas en place un agent autonome : c'est volontaire pour limiter les actions et les coûts.
