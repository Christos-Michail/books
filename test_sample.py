from app.models import Book, Author, Work


def test_make_Book():
    book = Book(key="sd4die",title="star wars")
    assert book.title == "star wars"


def test_makeaBookNoTitle():
    book = Book(key="sd4die")
    assert book.title is None

def test_book_author_reverse_relation():
    book = Book(key="sd4die")
    author = Author(key="dfs8fd8")
    author.books.append(book)
    assert author in book.authors

def test_book_work_relation():
    book = Book(key="sd4die")
    work = Work(key="dfwd8")
    book.works.append(work)
    assert work in book.works
