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

==========================================================================================================================*
# documentation tp 3 exo 4, 5 et 6

# biblio
EXERCICE 4

 """
    Service fournissant la logique métier pour la gestion des emprunts de livres dans un système de bibliothèque.
    Ce service gère la création, la récupération, la prolongation et le retour des emprunts, en appliquant des règles telles que le statut de l'utilisateur, la disponibilité des livres, la limite d'emprunts et la vérification des retards.

    Méthodes
    --------
    __init__(loan_repository, book_repository, user_repository)
        Initialise le LoanService avec les repositories pour les emprunts, les livres et les utilisateurs.
    get_active_loans() -> List[Loan]
        Récupère tous les emprunts actifs (non encore retournés).
    get_overdue_loans() -> List[Loan]
        Récupère tous les emprunts en retard.
    get_loans_by_user(*, user_id: int) -> List[Loan]
        Récupère tous les emprunts d'un utilisateur spécifique.
    get_loans_by_book(*, book_id: int) -> List[Loan]
        Récupère tous les emprunts d'un livre spécifique.
    create_loan(*, user_id: int, book_id: int, loan_period_days: int = 14) -> Loan
        Crée un nouvel emprunt après vérification du statut de l'utilisateur et du livre, des limites d'emprunt et des règles métier.
    return_loan(*, loan_id: int) -> Loan
        Marque un emprunt comme retourné et met à jour la quantité disponible du livre.
    extend_loan(*, loan_id: int, extension_days: int = 7) -> Loan
        Prolonge la date d'échéance d'un emprunt, en appliquant les règles sur les retards et les limites de prolongation.
    """

    EXERCICE 5
    
    CREATION DE ROUTES POUR UTILISER L API

    POUR LE SERVICE BOOKS

from sqlalchemy.orm import Session
from typing import List

from .base import BaseRepository
from ..models.books import Book


class BookRepository(BaseRepository[Book, None, None]):
    def get_by_isbn(self, db: Session, *, isbn: str) -> Book:
        """
        Récupère un livre par son ISBN.
        """
        return db.query(Book).filter(Book.isbn == isbn).first()

    def get_by_title(self, db: Session, *, title: str) -> List[Book]:
        """
        Récupère des livres par leur titre (recherche partielle).
        """
        return db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

    def get_by_author(self, db: Session, *, author: str) -> List[Book]:
        """
        Récupère des livres par leur auteur (recherche partielle).
        """
        return db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()


EXERCICE 6

MISE A JOUR DES DEPENDANCES

   """
    Dépendance pour obtenir l'utilisateur actuel à partir du token JWT.
    Décode le token JWT, valide sa charge utile et récupère l'utilisateur correspondant depuis la base de données.
    Lève des exceptions HTTP si le token est invalide ou si l'utilisateur n'existe pas.
    Args:
        db (Session): Session de base de données SQLAlchemy.
        token (str): Token JWT extrait de la requête.
    Returns:
        User: L'objet utilisateur authentifié.
    Raises:
        HTTPException: Si le token est invalide ou si l'utilisateur n'est pas trouvé.
    """
    """
    Dépendance pour obtenir l'utilisateur actuel à partir du token JWT.