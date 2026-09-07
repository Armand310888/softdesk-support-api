# SoftDesk Support API

SoftDesk est une API REST de suivi de problèmes techniques, développée dans le cadre d'une formation OpenClassrooms. Elle permet de gérer des projets, leurs contributeurs, leurs tâches/problèmes et leurs commentaires.

Le backend utilise Django REST Framework, SQLite en développement, Simple JWT pour l'authentification et drf-spectacular pour la documentation OpenAPI. Les dépendances sont gérées avec Poetry.

## Installation locale

### Prérequis

- Git
- Python compatible avec les dépendances du projet (la plage déclarée dans `pyproject.toml` est `>=3.12,<4.0`)
- Poetry

Les versions des dépendances résolues sont enregistrées dans `poetry.lock`.

Cloner le dépôt et installer les dépendances :

```bash
git clone https://github.com/Armand310888/softdesk-support-api.git
cd softdesk-support-api
poetry install
```

Toutes les commandes suivantes sont à exécuter depuis la racine du dépôt, qui contient `pyproject.toml`.

### Configuration

Créer un fichier `.env` à la racine du projet :

```dotenv
DJANGO_SECRET_KEY=replace-with-a-generated-secret-key
```

Pour générer une clé, exécuter la commande suivante et copier le résultat dans `.env` :

```bash
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Le fichier `.env` est ignoré par Git et ne doit pas être partagé. La configuration actuelle utilise `DEBUG=True` et SQLite : elle est destinée au développement local, pas à un déploiement en production.

### Base de données et serveur

```bash
poetry run python softdesk/manage.py migrate
poetry run python softdesk/manage.py runserver
```

La base SQLite est créée dans `softdesk/db.sqlite3` et reste hors du dépôt Git. Arrêter le serveur avec `Ctrl+C`.

Ouvrir directement la documentation : <http://127.0.0.1:8000/api/docs/>. Aucune page d'accueil n'est définie sur `/`.

Pour utiliser l'administration Django, créer facultativement un superutilisateur :

```bash
poetry run python softdesk/manage.py createsuperuser
```

L'administration est accessible sur <http://127.0.0.1:8000/admin/>. Un compte administrateur ne contourne pas automatiquement les permissions métier de l'API.

## Premiers pas avec l'API

### Créer un profil

Envoyer un `POST /api/users/` sans authentification, avec un corps JSON de cette forme. Remplacer les valeurs d'exemple et choisir un mot de passe accepté par les validateurs Django :

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "Replace-with-your-own-strong-password!",
  "age": 30,
  "can_be_contacted": false,
  "can_data_be_shared": false
}
```

Le nom d'utilisateur et l'adresse e-mail doivent être uniques. L'âge est obligatoire et compris entre 15 et 120 ans inclus. Chaque consentement doit être explicitement renseigné : `false` est une réponse valide. L'inscription est refusée à un utilisateur déjà authentifié ; dans Swagger UI, retirer l'autorisation active avant cet essai.

Conserver l'identifiant renvoyé à la création pour consulter ou modifier son propre profil.

### Obtenir et utiliser un jeton JWT

Envoyer un `POST /api/token/` :

```json
{
  "username": "alice",
  "password": "Replace-with-your-own-strong-password!"
}
```

La réponse contient `access` et `refresh`. Pour les opérations authentifiées, envoyer :

```http
Authorization: Bearer <access>
```

Dans Swagger UI, cliquer sur **Authorize**, coller uniquement la valeur de `access` sans guillemets ni préfixe `Bearer`, puis valider. Utiliser **Try it out**, puis **Execute**, pour lancer une requête. Obtenir un nouveau jeton ne remplace pas automatiquement celui enregistré dans **Authorize**.

Le jeton d'accès expire après 5 minutes. Pour le renouveler, envoyer un `POST /api/token/refresh/` :

```json
{
  "refresh": "<refresh>"
}
```

La rotation est activée : conserver les nouveaux jetons renvoyés, car l'ancien jeton de rafraîchissement est placé en liste noire. La durée configurée d'un jeton de rafraîchissement est d'un jour. Aucun endpoint de déconnexion avec révocation explicite n'est implémenté.

### Créer un premier projet

Avec un jeton d'accès valide, envoyer un `POST /api/projects/` :

```json
{
  "name": "Application mobile",
  "description": "Suivi des problèmes de l'application",
  "project_type": "ANDROID"
}
```

La description est facultative. Le compte connecté devient automatiquement auteur et contributeur du projet. Les opérations suivantes, notamment l'ajout de contributeurs par leur `username`, sont décrites dans Swagger UI.

## Documentation de l'API

| Adresse locale | Usage |
|---|---|
| [Swagger UI](http://127.0.0.1:8000/api/docs/) | Inventaire des endpoints, paramètres, schémas et essais manuels |
| [Schéma OpenAPI](http://127.0.0.1:8000/api/schema/) | Document exploitable par des outils, notamment pour un import dans Postman |

Quelques particularités à connaître avant les essais :

- Les listes globales des utilisateurs et projets sont désactivées. Les listes disponibles sont paginées par 10 ressources (`?page=2` pour la deuxième page).
- Les modifications utilisent `PATCH`. Seul le propriétaire accède à son profil ; l'accès aux ressources d'un projet est réservé à ses contributeurs.
- `DELETE` sur un profil anonymise et désactive le compte, retire ses appartenances et assignations, mais conserve ses ressources. Aucun transfert automatique des projets n'est prévu.
- Supprimer un projet supprime aussi ses issues et leurs commentaires ; supprimer une issue supprime ses commentaires.

Le [carnet de bord](CARNET_DE_BORD.md) précise les règles de permission, leurs exceptions et les choix de conception. Les exemples Swagger sont illustratifs et ne représentent pas les données présentes en base.

## Vérifications et maintenance

Contrôler la configuration Django et vérifier qu'aucune migration de modèle ne manque :

```bash
poetry run python softdesk/manage.py check
poetry run python softdesk/manage.py makemigrations --check --dry-run
```

Générer et valider le schéma OpenAPI, en faisant échouer la commande en présence d'avertissements :

```bash
poetry run python softdesk/manage.py spectacular --file /tmp/softdesk-schema.yaml --validate --fail-on-warn
```

Adapter le chemin de sortie si nécessaire. Les routes de documentation génèrent le schéma depuis le code ; un fichier exporté doit être régénéré après modification.

La validation OpenAPI contrôle le schéma, pas le comportement métier. Les tests automatisés restent à développer ; le bilan des essais manuels et les limites connues sont consignés dans le [carnet de bord](CARNET_DE_BORD.md).

## Organisation du dépôt

```text
softdesk/
├── manage.py
├── softdesk/       # Configuration Django et routes
├── users/          # Profils, consentements et authentification
└── projects/       # Projets, contributeurs, issues et commentaires
docs/              # Documents de référence du projet
CARNET_DE_BORD.md   # Exigences résumées, décisions et progression
```

Le [carnet de bord](CARNET_DE_BORD.md) détaille les décisions, les vérifications réalisées et les arbitrages ouverts, notamment la gestion des projets après anonymisation de leur auteur. Les documents de référence sont disponibles dans [docs/](docs/).
