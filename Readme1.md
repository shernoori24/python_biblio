## TP3 : Couche métier - Exercices 4, 5 et 6

### **Contexte**
Dans le cadre du TP3, nous avons implémenté et intégré la couche métier de l'application de gestion de bibliothèque. Les exercices 4, 5 et 6 se concentrent sur la gestion des emprunts, l’utilisation des services dans les routes API, et la sécurisation via des dépendances d’authentification.

### **Exercice 4 : Service d’emprunts**
**Objectif** : Implémenter `LoanService` pour gérer les emprunts avec des règles métier complexes.

- **Fichier** : `src/services/loans.py`
- **Fonctionnalités** :
  - Création d’emprunts avec vérification de la disponibilité des livres, du statut actif des utilisateurs, et de la limite de 5 emprunts.
  - Retour d’emprunts avec mise à jour de la quantité des livres.
  - Prolongation d’emprunts (une seule fois, pas pour les emprunts en retard).
- **Règles métier** :
  - Utilisateur actif requis.
  - Livre disponible (`quantity > 0`).
  - Pas d’emprunt multiple du même livre.
  - Limite de 5 emprunts actifs par utilisateur.
- **Pourquoi ?** Encapsule la logique métier des emprunts, garantissant cohérence et maintenabilité.

### **Exercice 5 : Mise à jour des routes API**
**Objectif** : Mettre à jour les routes pour utiliser `BookService`, `UserService`, et `LoanService`.

- **Fichiers** :
  - `src/api/routes/books.py` : Endpoints pour livres (CRUD, recherches).
  - `src/api/routes/users.py` : Endpoints pour utilisateurs (CRUD, profil `/me`).
  - `src/api/routes/loans.py` : Endpoints pour emprunts (création, retour, prolongation, listes).
- **Changements** :
  - Remplacement des accès directs aux repositories par des appels aux services.
  - Gestion des erreurs via `HTTPException` pour les `ValueError` des services.
  - Sécurisation des endpoints avec `get_current_active_user` et `get_current_admin_user`.
- **Pourquoi ?** Sépare la logique métier (services) de la présentation (routes), respectant les principes SOLID.

### **Exercice 6 : Mise à jour des dépendances d’authentification**
**Objectif** : Intégrer `UserService` dans la gestion de l’authentification JWT.

- **Fichier** : `src/api/dependencies.py`
- **Changements** :
  - Utilisation de `UserService` pour récupérer l’utilisateur à partir du token JWT.
  - Dépendances `get_current_active_user` et `get_current_admin_user` pour vérifier le statut actif et les privilèges admin.
- **Pourquoi ?** Maintient la cohérence avec la couche métier et sécurise les accès aux endpoints.

### **Exécution**
Pour tester les modifications :
```bash
uvicorn src.main:app --reload