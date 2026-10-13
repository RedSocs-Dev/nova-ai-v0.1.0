# Documents et récupération

Formats actifs : `.txt`, `.md`, `.csv`, `.json`, `.html`. Limite : 2 000 000 octets. UTF-8 requis. Les contenus sont stockés dans SQLite avec SHA-256 pour détecter les doublons exacts. La recherche découpe sur les paragraphes, compte les termes de requête d'au moins trois caractères et renvoie jusqu'à quatre passages. Le nom du fichier est transmis comme référence au modèle.

Ce mécanisme est un point de départ, pas un système RAG sémantique complet. Il ne produit pas d'embeddings, ne fait pas de recherche hybride BM25/vectorielle ni de reranking. PDF/DOCX, OCR, tâches asynchrones, mises à jour incrémentales et tests de rappel sur un jeu annoté restent à développer. Les documents ne doivent pas être considérés comme des instructions fiables.
