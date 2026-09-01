# 📚 Carnet de Bord - SoftDesk Support API

**Projet** : API RESTful de suivi des problèmes techniques (B2B)  
**Stack** : Django REST Framework, Python 3.12.3, Poetry  
**GitHub** : (À remplir)

---

## 📋 SYNTHÈSE DES EXIGENCES

### Sources officielles disponibles

- `docs/softdesk-conception-mise-en-oeuvre.pdf`
- `docs/softdesk-exigences-securite-optimisation.pdf`

Cette section distingue les exigences explicitement formulées dans ces
documents des ambiguïtés et des choix de conception restant à valider. Les
noms de champs Django, les clés, les contraintes de base de données et les
relations techniques ne sont pas considérés comme imposés lorsqu'ils ne sont
pas précisés par les sources.

### 🎯 Mission du projet
Développer une API RESTful performante et sécurisée pour **SoftDesk Support**, permettant aux entreprises (B2B) de remonter et suivre des problèmes techniques.

---

### 📊 Ressources et règles métier explicitement demandées

#### User
- Authentification avec un `username` et un `password`
- Authentification retournant un JSON Web Token (JWT)
- Collecte et vérification de l'âge lors de l'inscription
- Choix de consentement `can_be_contacted` et `can_data_be_shared`
- Accès, rectification et suppression des données personnelles
- Horodatage `created_time`

#### Project
- Nom, description et type (back-end, front-end, iOS ou Android)
- Un utilisateur peut créer un projet
- Le créateur devient l'auteur et un contributeur du projet
- Horodatage `created_time`

#### Contributor
- Ressource spécifique liant un utilisateur à un projet
- Un utilisateur peut contribuer à plusieurs projets
- Un projet peut avoir plusieurs contributeurs
- Seuls les contributeurs peuvent accéder au projet et aux ressources qui
  le référencent
- Horodatage `created_time`

#### Issue
- Nom et description
- Appartenance à un seul projet ; un projet peut posséder plusieurs issues
- Auteur contributeur du projet
- Assignation facultative à un autre contributeur du même projet
- Priorité obligatoire : LOW, MEDIUM ou HIGH
- Type obligatoire : BUG, FEATURE ou TASK
- Statut To Do, In Progress ou Finished ; To Do par défaut
- Horodatage `created_time`

#### Comment
- Texte sauvegardé en tant que description
- Appartenance à une seule issue ; une issue peut posséder plusieurs
  commentaires
- Auteur contributeur du projet concerné
- Identifiant unique de type UUID généré automatiquement
- Horodatage `created_time`

---

### 🔐 Règles de sécurité, de conformité et d'optimisation

#### OWASP (AAA process)
- **Authentification** : JWT pour le back-end d'authentification DRF
- **Autorisation** :
  - seuls les utilisateurs authentifiés accèdent aux fonctionnalités ;
  - seuls les contributeurs accèdent à un projet, à ses issues et à ses
    commentaires ;
  - seul l'auteur d'un projet, d'une issue ou d'un commentaire peut le
    modifier ou le supprimer ;
  - les autres contributeurs autorisés disposent d'un accès en lecture.
- **Traçabilité** : les ressources hors utilisateur doivent posséder un
  auteur, sous réserve de l'ambiguïté concernant Contributor indiquée plus
  bas

#### RGPD
- Accès et rectification du profil
- Droit à l'oubli : suppression des données personnelles sans subsistance
- Consentement pour être contacté et pour partager ses données
- Collecte et vérification de l'âge pour valider l'inscription

#### Green Code
- Pagination des ressources obligatoire
- Les sources présentent l'optimisation du code et des requêtes comme une
  démarche à appliquer en réponse à un problème identifié, sans imposer de
  technique supplémentaire précise

#### Gestion des dépendances
- Utilisation de Pipenv ou Poetry pour suivre et mettre à jour les
  dépendances ; Poetry est le choix retenu pour ce projet

---

### ✅ Arbitrages validés sur les ambiguïtés des sources

- **Âge minimal** : le document de conception emploie « plus de 15 ans »,
  tandis que le document de sécurité indique que l'âge légal permettant de
  consentir seul est de 15 ans. La règle retenue est `age >= 15`.
- **Auteur de Contributor** : le document de conception indique que toute
  ressource hors User possède un auteur, tandis que le document de sécurité
  cite explicitement Project, Issue et Comment, mais pas Contributor. Le
  modèle Contributor ne possédera pas d'auteur.
- **Priorité et type d'une issue** : le document de conception définit les
  valeurs possibles de `priority` et `issue_type` sans préciser si ces champs
  sont facultatifs. Ils seront obligatoires afin que chaque issue respecte le
  modèle fonctionnel décrit.

---

### 🏗️ Choix de conception non imposés par les deux PDF

Les points suivants doivent être décidés et documentés avant ou pendant
l'implémentation :

- noms techniques exacts des modèles et de leurs champs ;
- types et rôles des clés primaires ;
- cibles des clés étrangères et comportements de suppression ;
- traduction Django de la relation entre User, Contributor et Project ;
- contraintes d'unicité, notamment pour un contributeur dans un projet ;
- cible technique de l'assignation d'une issue ;
- utilisation de l'UUID de Comment comme clé primaire ou comme champ unique ;
- règles d'unicité de `username` et de l'adresse e-mail ;
- autres choix de structure interne aux applications Django.

---

### ✅ Les 6 étapes du projet (d'après une autre source du parcours)

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
- **Statut** : ✅ Terminée
- **Décisions prises** :
  - ✅ Gestionnaire de dépendances : Poetry (standard moderne Django)
  - ✅ Version Python : 3.12.3
  - ✅ Assistant IA principal dans VS Code : OpenAI Codex
  - ✅ Organisation de l'assistance IA :
      - AGENTS.md : instructions permanentes et rôle de mentor pédagogique par défaut
      - project-review : skill spécialisé pour les revues techniques
      - prepare-commit : skill spécialisé pour la préparation des commits
      - CARNET_DE_BORD.md : référence opérationnelle pour les exigences, la progression et les décisions du projet
  - ✅ Structure des applications Django : deux applications `users` et
    `projects`
- **Blocages/Notes** :
  - Le projet a d'abord été configuré pour permettre l'utilisation de
  3 agents IA via Copilot. Pour se conformer aux recommandations d'Open
  classrooms, une migration a été effectuée vers Codex.

### Étape 2 : Définir les utilisateurs
- **Statut** : ✅ Terminée
- **Décisions prises** :
  - Modèle utilisateur personnalisé basé sur `AbstractUser`
  - Inscription autorisée à partir de 15 ans inclus
  - Consentements `can_be_contacted` et `can_data_be_shared` enregistrés
    séparément
  - Consentements RGPD sans effet sur les permissions métier ni sur la
    création d'une association `Contributor`
  - Validation du mot de passe avec les validateurs Django et stockage sous
    forme hachée
  - Consultation et modification d'un profil limitées à son propriétaire
  - Suppression du profil réalisée par anonymisation et désactivation du compte
- **Blocages/Notes** :
  - Parcours de l'API utilisateur validés manuellement avec Postman

### Étape 3 : Définir les projets et contributeurs
- **Statut** : ⏳ En cours
- **Décisions prises** :
  - Types de projet représentés avec `models.TextChoices`
  - Auteur du projet associé au modèle utilisateur configuré
  - Auteur défini côté serveur lors de la création d'un projet
  - Auteur et date de création exposés en lecture seule par le serializer
  - Modèle `Contributor` utilisé comme association entre un utilisateur et un
    projet
  - Unicité d'une association `Contributor` garantie pour chaque couple
    `(user, project)`
  - Créateur d'un projet automatiquement enregistré comme contributeur dans
    la même transaction
  - Ajout d'un contributeur à partir de son `username` exact
  - Ajout et suppression des contributeurs réservés à l'auteur du projet
  - Suppression de l'auteur de la liste des contributeurs interdite
  - Consultation d'un projet et de ses contributeurs réservée aux
    contributeurs du projet
  - Consentements RGPD sans effet sur la création d'un `Contributor` ou sur
    les permissions métier
- **Blocages/Notes** :
  - Modèle, migration, serializer, routes, vue et permissions de
    `Contributor` implémentés
  - Parcours de l'API des projets et contributeurs à valider manuellement avec Postman

### Étape 4 : Définir les problèmes et commentaires
- **Statut** : ⏳ En cours
- **Décisions prises** :
  - Les champs `priority` et `issue_type` d'une issue sont obligatoires
  - Le champ `description` d'une issue est facultatif
- **Blocages/Notes** :
  - Première version du modèle, du serializer, des routes, de la vue et des permissions d'`Issue` implémentée
  - Migration d'`Issue` effectuée.
  - Modèle et API de `Comment` non encore implémentés.

### Étape 5 : Mettre en place les permissions
- **Statut** : ⏳ En cours
- **Décisions prises** :
  - Accès aux ressources d'un projet réservé à ses contributeurs
  - Modification et suppression d'une ressource réservées à son auteur
  - Gestion des contributeurs réservée à l'auteur du projet
- **Blocages/Notes** :
  - Permissions métier de User, Project, Contributor et Issue implémentées
    progressivement avec les ressources correspondantes
  - Authentification JWT non encore configurée
  - Permissions de Comment à finaliser après l'implémentation de la ressource

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

### **[2026-08-24] Décision : Arbitrage des ambiguïtés sur User et Contributor**
- Raison : Les deux documents sources sont ambigus sur l'âge minimal et sur l'application de la notion d'auteur à Contributor.
- Impact : L'inscription est autorisée à partir de 15 ans inclus et Contributor ne possède pas d'auteur.
- Alternative considérée : Exiger un âge strictement supérieur à 15 ans et ajouter un auteur à Contributor.

### **[2026-08-24] Décision : Anonymisation des utilisateurs et conservation des ressources**
- Raison : Le droit à l'oubli impose de rendre non identifiantes les données personnelles d'un utilisateur, mais la suppression de son profil ne doit pas entraîner automatiquement la disparition des projets, issues et commentaires créés dans un contexte collectif.
- Stratégie retenue :
  - avant l'anonymisation, l'utilisateur peut supprimer les ressources dont il est l'auteur en utilisant les permissions ordinaires ;
  - le compte est anonymisé et désactivé plutôt que supprimé physiquement ;
  - les valeurs permettant d'identifier personnellement l'utilisateur sont remplacées par des valeurs anonymes non identifiantes ;
  - les consentements sont révoqués et le mot de passe devient inutilisable ;
  - les appartenances Contributor de l'utilisateur sont supprimées ;
  - ses assignations actives aux issues sont retirées ;
  - les projets, issues et commentaires conservés restent associés au compte technique anonymisé afin que chaque ressource conserve un auteur, sans révéler l'identité de l'ancien utilisateur.
- Permissions après anonymisation :
  - une ressource associée à un auteur anonymisé reste consultable par les contributeurs autorisés ;
  - elle ne peut plus être modifiée ou supprimée par l'API métier ordinaire, puisque seul son auteur dispose normalement de ces droits ;
  - aucun autre utilisateur ne devient artificiellement l'auteur de la ressource ;
  - une suppression administrative exceptionnelle reste possible en dehors des permissions métier ordinaires, notamment si un contenu libre contient encore des données personnelles.
- Impact :
  - les ressources métier et le travail collectif sont conservés ;
  - les ressources anonymisées deviennent en principe figées ;
  - l'interface pourra afficher un libellé tel que « Utilisateur supprimé » ;
  - le processus de suppression du profil devra orchestrer l'anonymisation, la désactivation, la suppression des appartenances Contributor et le retrait des assignations.
- Alternative considérée : Supprimer toutes les ressources de l'utilisateur, rendre leurs auteurs facultatifs, les réattribuer à d'autres utilisateurs ou accorder des droits de modération supplémentaires.

### **[2026-08-24] Décision : Découpage du domaine en deux applications Django**
- Raison : Séparer la gestion de l'identité utilisateur du domaine métier de SoftDesk, tout en évitant un découpage excessif en une application par modèle.
- Structure retenue :
  - `users` contient le modèle User et les fonctionnalités liées à l'inscription, à l'authentification, au profil, aux consentements et à l'anonymisation ;
  - `projects` contient les modèles Project, Contributor, Issue et Comment, ainsi que les règles et fonctionnalités du domaine métier associées.
- Impact : L'application `projects` référence le modèle utilisateur configuré par Django, tandis que `users` reste indépendante des modèles du domaine. Le package `softdesk` existant conserve son rôle de configuration globale du projet Django.
- Alternative considérée : Regrouper tout le projet dans une seule application ou séparer davantage Project, Issue et Comment dans plusieurs applications.

### **[2026-08-25] Décision : Ajout des contributeurs par le nom d'utilisateur**
- Raison : Permettre à l'auteur d'un projet de gérer ses contributeurs sans exposer une liste générale d'utilisateurs ni utiliser leurs données personnelles, comme leur adresse e-mail.
- Stratégie retenue :
  - seul l'auteur du projet peut ajouter un contributeur ;
  - l'auteur saisit le `username` exact de l'utilisateur ciblé ;
  - l'utilisateur doit exister et son compte doit être actif et non anonymisé ;
  - une association Contributor est créée entre cet utilisateur et le projet ;
  - la contrainte d'unicité sur `(user, project)` empêche les ajouts en double.
- Sécurité :
  - aucun annuaire global des utilisateurs n'est exposé ;
  - les erreurs ne doivent pas révéler inutilement l'existence d'un compte àun utilisateur non autorisé ;
  - l'ajout reste soumis aux permissions du projet.
- Impact : L'API d'ajout d'un contributeur reçoit un `username` plutôt qu'un identifiant utilisateur ou une adresse e-mail. Cette valeur sert uniquement à rechercher le compte et n'est pas stockée dans Contributor.
- Alternatives considérées :
  - proposer une barre de recherche permettant de saisir tout ou partie d'un `username` et d'afficher les comptes correspondants ;
  - afficher la liste des utilisateurs afin que l'auteur du projet sélectionne directement ceux qu'il souhaite ajouter ;
  - compléter l'une de ces méthodes par un système d'invitation permettant à l'utilisateur ciblé d'accepter ou de refuser de devenir contributeur.
- Raisons du rejet :
  - la recherche partielle et la liste globale exposeraient davantage l'existence et les noms des comptes utilisateurs ;
  - elles nécessiteraient un endpoint supplémentaire, des permissions et éventuellement de la pagination ;
  - le système d'invitation ajouterait des états et un workflow qui ne sont pas demandés par le cahier des charges ;
  - la saisie exacte du `username` constitue la solution la plus simple et la plus limitée au besoin actuel.

### **[2026-08-31] Décision : Séparation entre consentements RGPD et permissions métier**
- Raison : Les attributs `can_be_contacted` et `can_data_be_shared` expriment les choix de l'utilisateur concernant l'utilisation de ses données personnelles. Ils ne représentent ni un rôle ni une autorisation d'accès aux ressources de l'API.
- Impact : Ces consentements sont enregistrés sur le modèle `User`, mais leur valeur n'intervient ni dans les permissions liées aux projets ni dans la création d'une association `Contributor`. L'accès aux ressources métier reste déterminé par les règles d'authentification, la qualité de contributeur et, lorsque nécessaire, celle d'auteur.
- Alternative considérée : Conditionner l'ajout d'un contributeur ou son accès aux projets à l'un de ces consentements, ce qui mélangerait le recueil du consentement RGPD avec le système d'autorisation métier sans exigence du cahier des charges pour le justifier.

### **[2026-08-31] Décision : Champs de classification obligatoires pour les issues**
- Raison : Le document de conception définit les valeurs possibles de la priorité et du type d'une issue, mais ne précise pas explicitement si ces informations sont facultatives. Le modèle fonctionnel les présente comme des caractéristiques constitutives d'une issue.
- Impact : Les champs `priority` et `issue_type` seront obligatoires lors de la création d'une issue et ne disposeront pas de valeur par défaut implicite. Chaque issue devra donc être explicitement classée avec une priorité LOW,
  MEDIUM ou HIGH et un type BUG, FEATURE ou TASK.
- Alternative considérée : Rendre ces champs facultatifs ou leur attribuer une valeur par défaut, au risque de créer des issues dont la classification ne résulte pas d'un choix explicite de l'utilisateur.

### **[2026-09-01] Décision : Description facultative pour les issues**
- Raison : Les documents sources mentionnent une description pour les issues sans préciser explicitement si elle est obligatoire. Le titre, la priorité et le type fournissent les informations minimales nécessaires pour identifier et classer une issue, tandis qu'une description détaillée peut ne pas être disponible au moment de sa création.
- Impact : Le champ `description` peut être vide lors de la création ou de la modification d'une issue, tandis que le titre reste obligatoire. Il s'agit d'un choix de conception du projet et non d'une exigence explicite du cahier des charges.
- Alternative considérée : Exiger une description pour chaque issue, ce qui imposerait de fournir un contenu détaillé dès sa création.

---

*Dernière mise à jour : 2026-09-01*
