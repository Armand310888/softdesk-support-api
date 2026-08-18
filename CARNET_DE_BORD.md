# 📚 Carnet de Bord - SoftDesk Support API

**Projet** : API RESTful de suivi des problèmes techniques (B2B)  
**Stack** : Django REST Framework, Python 3.12.3, Poetry  
**GitHub** : (À remplir)

---

## 📋 SYNTHÈSE DE L'ÉNONCÉ

### 🎯 Mission du projet
Développer une API RESTful performante et sécurisée pour **SoftDesk Support**, permettant aux entreprises (B2B) de remonter et suivre des problèmes techniques.

---

### 📊 Modèles de données (d'après l'énoncé)

#### User
- `username`, `password` (authentification)
- `age` (vérification RGPD : >= 15 ans obligatoire)
- `can_be_contacted` (RGPD)
- `can_data_be_shared` (RGPD)
- Horodatage : `created_time`

#### Project
- `name`, `description`, `type` (back-end, front-end, iOS, Android)
- `author` (clé étrangère User)
- Horodatage : `created_time`

#### Contributor
- `user` (clé étrangère)
- `project` (clé étrangère)
- Lie un utilisateur à un projet
- Relation many-to-many

#### Issue
- `title`, `description`
- `status` (To Do, In Progress, Finished) — par défaut: To Do
- `priority` (LOW, MEDIUM, HIGH)
- `tag` (BUG, FEATURE, TASK)
- `project` (clé étrangère)
- `author` (clé étrangère User)
- `assigned_to` (clé étrangère User, pour assigner à un contributeur)
- Horodatage : `created_time`

#### Comment
- `description`
- `author` (clé étrangère User)
- `issue` (clé étrangère)
- `uuid` (identifiant unique auto-généré)
- Horodatage : `created_time`

---

### 🔐 Règles de sécurité et conformité (d'après l'énoncé)

#### OWASP (AAA process)
- **Authentication** : JWT pour l'authentification
- **Authorization** : 
  - Seuls utilisateurs authentifiés accèdent à l'application
  - Un utilisateur ne doit pas accéder à un projet s'il n'est pas contributeur
  - L'auteur d'une ressource peut la modifier/supprimer; les autres ne peuvent que la lire
- **Accounting** : Chaque ressource (hors User) doit avoir un `author`

#### RGPD
- Vérification d'âge >= 15 ans à l'inscription
- Champs de consentement : `can_be_contacted`, `can_data_be_shared`
- Droit à l'oubli : suppression complète des données personnelles

#### Green Code
- Pagination des ressources obligatoire
- Optimisation des requêtes (éviter N+1)
- Pas d'imbrication excessive des ressources

---

### ✅ Les 6 étapes du projet (d'après l'énoncé)

**Étape 0** : Recommandations générales
- Bien cadrer avant de coder
- Étudier ModelViewsets de DRF
- Définir une stratégie de tests (user journeys)

**Étape 1** : Démarrer le projet et identifier le besoin
- Prérequis : Étudier l'énoncé et le diagramme
- Résultats attendus : Structure Django + Git/GitHub + README

**Étape 2** : Définir les utilisateurs
- Prérequis : Étape 1 complétée
- Résultats attendus : User model implémenté + testable avec Postman

**Étape 3** : Définir les projets et contributeurs
- Prérequis : Étape 2 complétée
- Résultats attendus : Project et Contributor models implémentés + testés

**Étape 4** : Définir les problèmes et commentaires
- Prérequis : Étape 3 complétée
- Résultats attendus : Issue et Comment models implémentés + testés

**Étape 5** : Mettre en place le système de permissions
- Prérequis : Toutes les étapes précédentes complétées
- Résultats attendus : JWT + Permission classes implémentées + GitHub Dependabot activé

**Étape 6** : Penser "Green Code" et optimiser
- Prérequis : Étapes 1-5 complétées
- Résultats attendus : Pagination implémentée + requêtes optimisées

---

## ✅ PROGRESSION DU PROJET

### Étape 1 : Démarrer le projet et identifier le besoin
- **Statut** : ⏳ En cours
- **Décisions prises** :
  - ✅ Gestionnaire de dépendances : Poetry (standard moderne Django)
  - ✅ Version Python : 3.12.3
  - ✅ Assistant IA principal dans VS Code : OpenAI Codex
  - ✅ Organisation de l'assistance IA :
      - AGENTS.md : instructions permanentes et rôle de mentor pédagogique par défaut
      - project-review : skill spécialisé pour les revues techniques
      - prepare-commit : skill spécialisé pour la préparation des commits
      - CARNET_DE_BORD.md : référence opérationnelle pour les exigences, la progression et les décisions du projet
  - ⏳ Structure des applications Django : à définir
- **Blocages/Notes** :
  - Le projet a d'abord été configuré pour permettre l'utilisation de
  3 agents IA via Copilot. Pour se conformer aux recommandations d'Open
  classrooms, une migration a été effectuée vers Codex.

### Étape 2 : Définir les utilisateurs
- **Statut** : ❌ Pas commencé
- **Décisions prises** : (À remplir)
- **Blocages/Notes** : (À remplir)

### Étape 3 : Définir les projets et contributeurs
- **Statut** : ❌ Pas commencé
- **Décisions prises** : (À remplir)
- **Blocages/Notes** : (À remplir)

### Étape 4 : Définir les problèmes et commentaires
- **Statut** : ❌ Pas commencé
- **Décisions prises** : (À remplir)
- **Blocages/Notes** : (À remplir)

### Étape 5 : Mettre en place les permissions
- **Statut** : ❌ Pas commencé
- **Décisions prises** : (À remplir)
- **Blocages/Notes** : (À remplir)

### Étape 6 : Green Code et optimisation
- **Statut** : ❌ Pas commencé
- **Décisions prises** : (À remplir)
- **Blocages/Notes** : (À remplir)

---

## 📝 JOURNAL DES DÉCISIONS ARCHITECTURALES

*(À remplir au fur et à mesure du développement)*

**Format à utiliser** :
```
**[DATE] Décision : Intitulé**
- Raison : Pourquoi ce choix ?
- Impact : Conséquences sur le projet
- Alternative considérée : (si applicable)
```

### **[2026-08-18] Décision : Mise en place d’une architecture IA en 3 agents**
- Raison : Séparer les responsabilités pour guider l’apprentissage, sécuriser la qualité technique et organiser le travail Git, sans perdre la maîtrise de la décision humaine.
- Impact : Le workflow est désormais structuré en trois rôles distincts : un mentor par défaut, un agent de revue technique et un agent de préparation de commits.
- Alternative considérée : Un seul agent généraliste, mais il serait plus difficile de maintenir une pédagogie claire, des priorités de revue cohérentes et un bon contrôle Git.

#### Agent mentor
- Objectif : accompagner le développement de manière pédagogique, sans prendre le lead sur la conception ni anticiper les étapes suivantes.
- Rôle par défaut : répondre en priorité comme un mentor personnel, poser des questions ciblées, donner des indices et corriger doucement.
- Comportement attendu : laisser l’utilisateur au centre de la décision, guider sans imposer, et favoriser l’autonomie.
- Limites : ne pas faire le travail à la place de l’utilisateur, ne pas anticiper la suite, ne pas imposer une architecture trop tôt.

#### Agent review
- Objectif : vérifier la qualité du code avant tout, avec une priorité absolue sur le bon fonctionnement du programme.
- Vérifications prioritaires : erreurs évidentes, imports inutilisés, code mort, mauvais nommage, logique incohérente, documentation insuffisante.
- Vérifications secondaires : refactorisation utile, choix de conception significatifs.
- Hors scope temporaire : tests, car la formation n’a pas encore atteint ce niveau de formalisation.
- Mode d’usage : revue sur demande ou vérification légère avant commit.

#### Agent commit
- Objectif : aider à organiser les changements par bloc logique et à rédiger des messages de commit conformes à la convention du projet.
- Règle clé : l’agent ne doit pas exécuter directement Git sans validation explicite de l’utilisateur.
- Il doit proposer un découpage logique, un message de commit structuré et une validation humaine avant tout staging ou commit.
- Convention attendue : `type(scope): description courte`.

---

*Dernière mise à jour : 2026-08-18*
