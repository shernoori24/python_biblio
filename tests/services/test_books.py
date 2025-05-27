import pytest
from sqlalchemy.orm import Session

from src.models.books import Book
from src.repositories.books import BookRepository
from src.services.books import BookService
from src.api.schemas.books import BookCreate, BookUpdate


def test_create_book(db_session: Session):
    """
    Teste la création d'un livre.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Test Book",
        author="Test Author",
        isbn="1234567890123",
        publication_year=2020,
        description="A test book",
        quantity=5
    )

    book = service.create(obj_in=book_in)

    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890123"
    assert book.publication_year == 2020
    assert book.description == "A test book"
    assert book.quantity == 5


def test_create_book_duplicate_isbn(db_session: Session):
    """
    Teste la création d'un livre avec un ISBN déjà utilisé.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Test Book",
        author="Test Author",
        isbn="1234567890123",
        publication_year=2020,
        quantity=5
    )

    service.create(obj_in=book_in)

    # Tentative de création avec le même ISBN
    with pytest.raises(ValueError, match="L'ISBN est déjà utilisé"):
        service.create(obj_in=book_in)


def test_get_by_isbn(db_session: Session):
    """
    Teste la récupération d'un livre par ISBN.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Test Book",
        author="Test Author",
        isbn="1234567890123",
        publication_year=2020,
        quantity=5
    )

    created_book = service.create(obj_in=book_in)

    # Récupération réussie
    book = service.get_by_isbn(isbn="1234567890123")
    assert book is not None
    assert book.id == created_book.id
    assert book.isbn == "1234567890123"

    # Récupération échouée - ISBN inexistant
    book = service.get_by_isbn(isbn="9999999999999")
    assert book is None


def test_get_by_title(db_session: Session):
    """
    Teste la recherche de livres par titre (recherche partielle).
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in1 = BookCreate(
        title="Python Programming",
        author="Author One",
        isbn="1111111111111",
        publication_year=2020,
        quantity=3
    )
    book_in2 = BookCreate(
        title="Advanced Python",
        author="Author Two",
        isbn="2222222222222",
        publication_year=2021,
        quantity=2
    )

    service.create(obj_in=book_in1)
    service.create(obj_in=book_in2)

    # Recherche par titre partiel
    books = service.get_by_title(title="Python")
    assert len(books) == 2
    assert any(book.title == "Python Programming" for book in books)
    assert any(book.title == "Advanced Python" for book in books)

    # Recherche sans résultat
    books = service.get_by_title(title="Java")
    assert len(books) == 0


def test_get_by_author(db_session: Session):
    """
    Teste la recherche de livres par auteur (recherche partielle).
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in1 = BookCreate(
        title="Book One",
        author="John Doe",
        isbn="3333333333333",
        publication_year=2020,
        quantity=3
    )
    book_in2 = BookCreate(
        title="Book Two",
        author="Jane Doe",
        isbn="4444444444444",
        publication_year=2021,
        quantity=2
    )

    service.create(obj_in=book_in1)
    service.create(obj_in=book_in2)

    # Recherche par auteur partiel
    books = service.get_by_author(author="Doe")
    assert len(books) == 2
    assert any(book.author == "John Doe" for book in books)
    assert any(book.author == "Jane Doe" for book in books)

    # Recherche sans résultat
    books = service.get_by_author(author="Smith")
    assert len(books) == 0


def test_update_quantity(db_session: Session):
    """
    Teste la mise à jour de la quantité d'un livre.
    """
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Test Book",
        author="Test Author",
        isbn="1234567890123",
        publication_year=2020,
        quantity=5
    )

    book = service.create(obj_in=book_in)

    # Augmenter la quantité
    updated_book = service.update_quantity(book_id=book.id, quantity_change=3)
    assert updated_book.quantity == 8

    # Diminuer la quantité
    updated_book = service.update_quantity(book_id=book.id, quantity_change=-2)
    assert updated_book.quantity == 6

    # Tentative de mise à jour avec quantité négative
    with pytest.raises(ValueError, match="La quantité ne peut pas être négative"):
        service.update_quantity(book_id=book.id, quantity_change=-10)

    # Tentative de mise à jour d’un livre inexistant
    with pytest.raises(ValueError, match="Livre avec l'ID 999 non trouvé"):
        service.update_quantity(book_id=999, quantity_change=1)