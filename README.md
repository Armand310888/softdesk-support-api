# SoftDesk Support API

SoftDesk est une API REST développée avec Django REST Framework. Elle permet de gérer des projets, leurs contributeurs, leurs problèmes techniques et les commentaires associés.

Le projet est actuellement en cours de développement.

## Prérequis

- Git
- Python 3.12
- Poetry

## Installation

Cloner le dépôt, puis se placer dans le dossier du projet :

```bash
git clone <git@github.com:Armand310888/softdesk-support-api.git>
cd project_10_SoftDesk
```

Installer les dépendances définies dans `pyproject.toml` :

```bash
poetry install
```

## Configuration

Créer un fichier `.env` à la racine du projet et y définir une clé secrète Django :

```dotenv
DJANGO_SECRET_KEY=replace-with-a-secure-random-value
```

Le fichier `.env` contient des informations sensibles et ne doit pas être ajouté au dépôt Git.

## Initialisation de la base de données

Appliquer les migrations Django :

```bash
poetry run python softdesk/manage.py migrate
```

## Lancement du serveur local

Démarrer le serveur de développement :

```bash
poetry run python softdesk/manage.py runserver
```

L'application est alors accessible à l'adresse
<http://127.0.0.1:8000/>.

Pour arrêter le serveur, utiliser `Ctrl+C` dans le terminal.
