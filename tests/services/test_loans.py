import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.models.loans import Loan
from src.models.books import Book
from src.models.users import User
from src.repositories.loans import LoanRepository
from src.repositories.books import BookRepository
from src.repositories.users import UserRepository
from src.services.loans import LoanService
from src.api.schemas.books import BookCreate
from src.api.schemas.users import UserCreate


@pytest.fixture
def create_user(db_session: Session):
    """
    Fixture pour créer un utilisateur.
    """
    repository = UserRepository(User, db_session)
    user_in = UserCreate(
        email="test@example.com",
        password="password123",
        full_name="Test User",
        is_active=True,
        is_admin=False
    )
    service = UserService(repository)
    return service.create(obj_in=user_in)


@pytest.fixture
def create_book(db_session: Session):
    """
    Fixture pour créer un livre.
    """
    repository = BookRepository(Book, db_session)
    book_in = BookCreate(
        title="Test Book",
        author="Test Author",
        isbn="1234567890123",
        publication_year=2020,
        quantity=5
    )
    service = BookService(repository)
    return service.create(obj_in=book_in)


def test_create_loan(db_session: Session, create_user, create_book):
    """
    Teste la création d’un emprunt.
    """
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    loan = service.create_loan(user_id=create_user.id, book_id=create_book.id)

    assert loan.user_id == create_user.id
    assert loan.book_id == create_book.id
    assert loan.loan_date is not None
    assert loan.due_date > loan.loan_date
    assert loan.return_date is None

    # Vérifier que la quantité du livre a diminué
    updated_book = book_repository.get(id=create_book.id)
    assert updated_book.quantity == create_book.quantity - 1


def test_create_loan_book_unavailable(db_session: Session, create_user, create_book):
    """
    Teste la création d’un emprunt avec un livre non disponible.
    """
    # Mettre la quantité à 0
    book_repository = BookRepository(Book, db_session)
    book_repository.update(db_obj=create_book, obj_in={"quantity": 0})

    loan_repository = LoanRepository(Loan, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    with pytest.raises(ValueError, match="Le livre n’est pas disponible pour l’emprunt"):
        service.create_loan(user_id=create_user.id, book_id=create_book.id)


def test_create_loan_inactive_user(db_session: Session, create_user, create_book):
    """
    Teste la création d’un emprunt avec un utilisateur inactif.
    """
    # Rendre l’utilisateur inactif
    user_repository = UserRepository(User, db_session)
    user_repository.update(db_obj=create_user, obj_in={"is_active": False})

    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    with pytest.raises(ValueError, match="L’utilisateur est inactif et ne peut pas emprunter de livres"):
        service.create_loan(user_id=create_user.id, book_id=create_book.id)


def test_create_loan_already_borrowed(db_session: Session, create_user, create_book):
    """
    Teste la création d’un emprunt pour un livre déjà emprunté par le même utilisateur.
    """
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    # Créer un premier emprunt
    service.create_loan(user_id=create_user.id, book_id=create_book.id)

    # Tenter de créer un autre emprunt pour le même livre
    with pytest.raises(ValueError, match="L’utilisateur a déjà emprunté ce livre et ne l’a pas encore rendu"):
        service.create_loan(user_id=create_user.id, book_id=create_book.id)


def test_create_loan_max_loans(db_session: Session, create_user):
    """
    Teste la création d’un emprunt lorsque l’utilisateur a atteint la limite d’emprunts.
    """
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    # Créer 5 livres
    books = []
    for i in range(5):
        book_in = BookCreate(
            title=f"Book {i}",
            author="Test Author",
            isbn=f"1234567890{i:03d}",
            publication_year=2020,
            quantity=1
        )
        book_service = BookService(book_repository)
        books.append(book_service.create(obj_in=book_in))

    # Créer 5 emprunts
    for book in books:
        service.create_loan(user_id=create_user.id, book_id=book.id)

    # Tenter de créer un 6ème emprunt
    new_book_in = BookCreate(
        title="New Book",
        author="Test Author",
        isbn="1234567890999",
        publication_year=2020,
        quantity=1
    )
    new_book = BookService(book_repository).create(obj_in=new_book_in)

    with pytest.raises(ValueError, match="L’utilisateur a atteint la limite d’emprunts simultanés"):
        service.create_loan(user_id=create_user.id, book_id=new_book.id)


def test_return_loan(db_session: Session, create_user, create_book):
    """
    Teste le retour d’un emprunt.
    """
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    loan = service.create_loan(user_id=create_user.id, book_id=create_book.id)

    returned_loan = service.return_loan(loan_id=loan.id)

    assert returned_loan.return_date is not None
    assert returned_loan.id == loan.id

    # Vérifier que la quantité du livre a été augmentée
    updated_book = book_repository.get(id=create_book.id)
    assert updated_book.quantity == create_book.quantity


def test_return_loan_already_returned(db_session: Session, create_user, create_book):
    """
    Teste le retour d’un emprunt déjà retourné.
    """
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    loan = service.create_loan(user_id=create_user.id, book_id=create_book.id)
    service.return_loan(loan_id=loan.id)

    with pytest.raises(ValueError, match="L’emprunt a déjà été retourné"):
        service.return_loan(loan_id=loan.id)


def test_extend_loan(db_session: Session, create_user, create_book):
    """
    Teste la prolongation d’un emprunt.
    """
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    loan = service.create_loan(user_id=create_user.id, book_id=create_book.id)

    extended_loan = service.extend_loan(loan_id=loan.id, extension_days=7)

    assert extended_loan.due_date == loan.due_date + timedelta(days=7)
    assert extended_loan.id == loan.id


def test_extend_loan_already_extended(db_session: Session, create_user, create_book):
    """
    Teste la prolongation d’un emprunt déjà prolongé.
    """
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    loan = service.create_loan(user_id=create_user.id, book_id=create_book.id)
    service.extend_loan(loan_id=loan.id, extension_days=7)

    with pytest.raises(ValueError, match="L’emprunt a déjà été prolongé"):
        service.extend_loan(loan_id=loan.id, extension_days=7)


def test_extend_loan_overdue(db_session: Session, create_user, create_book):
    """
    Teste la prolongation d’un emprunt en retard.
    """
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    # Créer un emprunt avec une date d’échéance passée
    loan_data = {
        "user_id": create_user.id,
        "book_id": create_book.id,
        "loan_date": datetime.utcnow() - timedelta(days=30),
        "due_date": datetime.utcnow() - timedelta(days=15),
        "return_date": None
    }
    loan = loan_repository.create(obj_in=loan_data)

    with pytest.raises(ValueError, match="L’emprunt est en retard et ne peut pas être prolongé"):
        service.extend_loan(loan_id=loan.id, extension_days=7)