# python_biblio


# Système de Gestion de Bibliothèque

Ce projet est une application de gestion de bibliothèque développée avec **FastAPI**, suivant une architecture **N-Tiers**. Il permet de gérer les livres, les utilisateurs et les emprunts. Cette section documente les **exercices 5 et 6** du **TP2**, qui concernent la mise à jour du point d'entrée de l'application et l'implémentation des modèles SQLAlchemy.

## Exercice 5 : Mise à jour du point d'entrée de l'application

### Objectif
Mettre à jour le fichier `src/main.py` pour :
- Intégrer les routes API définies dans les modules de routage.
- Configurer les paramètres CORS pour permettre les requêtes cross-origin.
- Importer les modèles SQLAlchemy pour permettre à Alembic de gérer les migrations de la base de données.

### Description
Le fichier `src/main.py` est le point d'entrée de l'application FastAPI. Il initialise l'application, configure les paramètres CORS, intègre les routes API et importe les modèles SQLAlchemy nécessaires.

### Détails du code
- **Fichier** : `src/main.py`
- **Dépendances** :
  - `fastapi` : Pour créer l'application API.
  - `fastapi.middleware.cors` : Pour configurer CORS.
  - `config.settings` : Pour accéder aux paramètres de configuration (nom du projet, préfixe API, etc.).
  - `api.routes.api_router` : Pour intégrer les routes API (livres, utilisateurs, emprunts, authentification).
  - `models.base`, `models.books`, `models.users`, `models.loans` : Pour importer les modèles SQLAlchemy utilisés par Alembic.
- **Fonctionnalités** :
  - Initialisation de l'application FastAPI avec le nom du projet et l'URL des spécifications OpenAPI.
  - Configuration CORS pour autoriser les requêtes depuis des domaines spécifiés (par exemple, `http://localhost:3000`).
  - Inclusion des routes API avec le préfixe `/api/v1`.
  - Définition d'une route racine (`/`) qui renvoie un message de bienvenue.

### Pourquoi ?
- **Intégration des routes** : Connecte les routes définies dans `src/api/routes` à l'application.
- **Support d'Alembic** : Les modèles importés permettent à Alembic de générer les migrations pour la base de données.
- **Sécurité CORS** : Évite les erreurs de sécurité dans les navigateurs lors de requêtes cross-origin.

---

## Exercice 6 : Implémentation des modèles SQLAlchemy

### Objectif
Définir les modèles SQLAlchemy pour les entités **livres**, **utilisateurs** et **emprunts**, qui représentent la structure des tables dans la base de données et établissent les relations entre elles.

### Description
Les modèles SQLAlchemy définissent la structure des tables de la base de données et permettent à l'application d'interagir avec la base de données via un ORM (Object-Relational Mapping). Chaque modèle correspond à une table et inclut des colonnes et des relations.

### Détails des fichiers

#### 1. `src/models/books.py`
- **Objectif** : Définir le modèle pour la table des livres.
- **Colonnes** :
  - `title` : Titre du livre (chaîne, 100 caractères max, non nul, indexé).
  - `author` : Auteur du livre (chaîne, 100 caractères max, non nul, indexé).
  - `isbn` : Code ISBN (chaîne, 13 caractères max, unique, indexé).
  - `publication_year` : Année de publication (entier, non nul).
  - `description` : Description du livre (texte, facultatif).
  - `quantity` : Nombre d'exemplaires disponibles (entier, non nul, défaut à 0).
- **Relations** :
  - `loans` : Relation un-à-plusieurs avec le modèle `Loan`. Si un livre est supprimé, ses emprunts associés sont également supprimés (`cascade="all, delete-orphan"`).

#### 2. `src/models/users.py`
- **Objectif** : Définir le modèle pour la table des utilisateurs.
- **Colonnes** :
  - `email` : Adresse email (chaîne, 100 caractères max, unique, indexée).
  - `hashed_password` : Mot de passe haché (chaîne, non nul).
  - `full_name` : Nom complet (chaîne, 100 caractères max, non nul).
  - `is_active` : Statut actif de l'utilisateur (booléen, défaut à `True`).
  - `is_admin` : Statut administrateur (booléen, défaut à `False`).
- **Relations** :
  - `loans` : Relation un-à-plusieurs avec le modèle `Loan`. Si un utilisateur est supprimé, ses emprunts associés sont également supprimés.

#### 3. `src/models/loans.py`
- **Objectif** : Définir le modèle pour la table des emprunts.
- **Colonnes** :
  - `user_id` : Clé étrangère vers la table `user` (entier, non nul).
  - `book_id` : Clé étrangère vers la table `book` (entier, non nul).
  - `loan_date` : Date de l'emprunt (date/heure, défaut à la date actuelle).
  - `return_date` : Date de retour (date/heure, facultatif).
  - `due_date` : Date d'échéance (date/heure, non nul).
- **Relations** :
  - `user` : Relation avec le modèle `User`.
  - `book` : Relation avec le modèle `Book`.

#### 4. `src/models/__init__.py`
- **Objectif** : Importer tous les modèles pour faciliter leur utilisation dans d'autres parties du projet (par exemple, dans `main.py` ou pour Alembic).
- **Contenu** : Importe les classes `Base`, `Book`, `User` et `Loan`.

### Pourquoi ?
- **Structure de la base de données** : Les modèles définissent les tables et leurs relations, permettant à SQLAlchemy de gérer les interactions avec la base de données.
- **Relations** : Les relations (comme `loans`) permettent un accès facile aux données associées (par exemple, les emprunts d'un livre).
- **Support d'Alembic** : Les modèles sont utilisés par Alembic pour générer les migrations qui créent les tables dans la base de données.

---

## Comment tester ?
1. Assurez-vous que les fichiers `src/main.py` et les modèles dans `src/models/` sont correctement configurés.
2. Lancez l'application avec :
   ```bash
   python run.py