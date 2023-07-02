import os
from . import create_app, db
from .models import Book, Author, Work
from flask import jsonify, request, abort
import requests

app = create_app('development')
with app.app_context():
    db.drop_all()
    db.create_all()
OPEN_LIBRARY="https://openlibrary.org"
BOOKS_API = "https://openlibrary.org/books/"
WORKS_API = "https://openlibrary.org/works/"
@app.route("/book/favourites", methods=["GET"])
def get_favourite_books():
    favourite_books=['OL7353617M', 'OL33145448M', 'OL1017798M']
    for book in favourite_books:
        responce = requests.get(BOOKS_API + book + '.json').json()
        book = Book(
            key=responce.get('key'),
            title=responce.get('title'),
            number_of_pages=responce.get('number_of_pages')
        )
        db.session.add(book)
        db.session.commit()
        for author in responce.get('authors'):
            author = requests.get(OPEN_LIBRARY + author.get('key') + '.json').json()
            author = Author(
                key=author.get('key'),
                personal_name=author.get('personal_name'),
                top_work=author.get('top_work')
            )
            author.books.append(book)
            db.session.add(author)
            db.session.commit()

        for work in responce.get('works'):
            work = requests.get(OPEN_LIBRARY + work.get('key') + '.json').json()
            work = Work(
                key=work.get('key'),
                title=work.get('title'),
                book_key=responce.get('key')
            )
            db.session.add(work)
            db.session.commit()
    books = Book.query.all()
    return jsonify([book.to_json() for book in books])