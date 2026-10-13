# NOVA AI — version 0.1.0

Assistant personnel modulaire : API FastAPI, interface web légère, stockage SQLite, historique conversationnel, mémoire explicite et import documentaire lexical. Cette version est un **socle fonctionnel**, pas un modèle d'IA entraîné par le projet.

## Audit de l'environnement de développement initial

Audit réalisé dans l'environnement d'exécution disponible pour la génération du projet :
- Linux x86_64 ; Python 3.13.5.
- Environ 5,81 Gio de RAM détectés et 29,83 Gio d'espace disque libre.
- PyTorch CPU présent ; aucun GPU CUDA détecté, `nvidia-smi` absent.
- FastAPI, Uvicorn, Pydantic, httpx, pytest et SQLAlchemy étaient détectables.
- Docker absent. Aucun nom de variable d'environnement identifié comme clé API n'a été affiché ni sa valeur inspectée.
- Cette mesure concerne l'environnement de construction, pas nécessairement l'ordinateur sur lequel vous installerez NOVA.
- La connectivité réseau, la présence de clés utilisables et l'accès à un service de modèle n'ont pas été validés.

## Fonctions présentes

- Interface responsive en français, historique et création/suppression/renommage de conversations.
- API FastAPI avec validation Pydantic et SQLite.
- Connecteur réel pour Ollama (`/api/chat`) et fournisseur OpenAI-compatible (`/v1/chat/completions`).
- Vérification de disponibilité du fournisseur.
- Mémoire explicitement enregistrée, consultable et effaçable.
- Import TXT, Markdown, CSV, JSON et HTML, contrôle de taille, UTF-8, SHA-256 et doublons.
- Recherche lexicale de passages documentaires et inclusion dans le contexte du modèle.
- Tests automatisés des API et du stockage.

## Installation locale

Python 3.11 ou plus récent est requis.

```bash
python -m venv .venv
# Linux/macOS :
source .venv/bin/activate
# Windows PowerShell :
# .venv\\Scripts\\Activate.ps1

python -m pip install -e ".[dev]"
cp .env.example .env
```

Sous Windows, copiez `.env.example` vers `.env` au lieu de `cp`.

### Option A — modèle local avec Ollama

Installez Ollama séparément depuis son site officiel, démarrez le service et téléchargez un modèle adapté à votre mémoire. Exemple :

```bash
ollama pull llama3.2
```

Dans `.env`, conservez `NOVA_PROVIDER=ollama`, `NOVA_BASE_URL=http://localhost:11434` et `NOVA_MODEL=llama3.2`. Le téléchargement du modèle nécessite Internet et de l'espace disque. Les performances dépendent du matériel.

### Option B — API compatible OpenAI

Configurez dans `.env` :
```dotenv
NOVA_PROVIDER=openai_compatible
NOVA_BASE_URL=https://votre-fournisseur.example
NOVA_MODEL=nom-du-modele
NOVA_API_KEY=votre-cle
```
Le nom de modèle, l'URL et la compatibilité doivent correspondre au fournisseur choisi. Le fichier `.env` est ignoré par Git ; ne partagez jamais cette clé.

### Lancer et tester

```bash
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Ouvrez `http://127.0.0.1:8000`. Documentation interactive de l'API : `http://127.0.0.1:8000/docs`.

Dans un second terminal :
```bash
python -m pytest
```

Diagnostic :
```bash
python scripts/health_check.py
```

## Configuration

Les paramètres sont préfixés par `NOVA_` et peuvent être définis dans l'environnement ou `.env` :
- `NOVA_NAME` : nom affiché dans les prompts et l'API.
- `NOVA_DATABASE_PATH` : chemin SQLite.
- `NOVA_PROVIDER` : `ollama` ou `openai_compatible`.
- `NOVA_MODEL`, `NOVA_BASE_URL`, `NOVA_API_KEY`.
- `NOVA_TIMEOUT_SECONDS`, `NOVA_MAX_INPUT_CHARS`.
- `NOVA_MEMORY_ENABLED`, `NOVA_CORS_ORIGINS`.

Ne mettez pas le serveur à disposition d'Internet sans ajouter authentification, HTTPS, limitation de débit robuste et isolation adaptée. Le serveur est volontairement recommandé sur `127.0.0.1`. La configuration CORS n'est pas une authentification.

## Architecture

Voir `docs/architecture.md`, `docs/security.md`, `docs/knowledge.md` et `docs/training.md`.

## Limites connues de cette version

- Le fournisseur doit être lancé et configuré séparément ; aucun modèle n'est livré et aucun appel à un modèle n'est réputé testé automatiquement.
- L'interface affiche la réponse après la fin de l'appel ; le streaming n'est pas implémenté.
- La mémoire est stockée et administrable, mais n'est pas encore injectée automatiquement dans les prompts.
- La recherche documentaire est lexicale, pas vectorielle ; elle découpe selon les paragraphes et peut manquer des passages pertinents.
- Les PDF/DOCX sont réservés à une extension ultérieure ; le socle accepte TXT/MD/CSV/JSON/HTML.
- Pas d'authentification multi-utilisateur, de sandbox de code, de recherche Web, de suivi financier, ni de fine-tuning opérationnel.
- Le renommage est accessible par clic droit sur une conversation dans l'interface.
- Les journaux ne consignent pas le corps des messages, mais les erreurs d'infrastructure sont seulement partiellement détaillées.

## Sauvegarde / restauration

Arrêtez l'application puis copiez le fichier SQLite indiqué par `NOVA_DATABASE_PATH` vers un emplacement protégé. Pour restaurer, arrêtez l'application et remplacez la base par la sauvegarde. Vérifiez d'abord la sauvegarde sur une copie. Le chiffrement au repos et les migrations versionnées ne sont pas encore fournis.

## Mise à jour

1. Sauvegardez la base et `.env`.
2. Examinez les changements et versions de dépendances.
3. Mettez à jour le code dans un environnement de test.
4. Exécutez `python -m pytest`.
5. Testez avec une copie de la base avant de mettre à jour la production.
6. Conservez la version précédente pour permettre un retour arrière.

## Coûts et ressources

- Code de ce dépôt : librement utilisable sous réserve des licences de ses dépendances.
- Ollama et les modèles locaux : coût d'API nul, mais calcul, énergie et stockage à votre charge ; les licences de modèles varient.
- Fournisseur distant : coût selon le fournisseur et le volume de tokens.
- Matériel observé pour l'environnement de construction : environ 5,81 Gio de RAM, CPU uniquement. Cela ne garantit pas que tous les modèles locaux puissent tourner.
