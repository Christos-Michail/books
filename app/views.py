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
            key=responce.get('key')[7:],
            title=responce.get('title'),
            number_of_pages=responce.get('number_of_pages')
        )
        db.session.add(book)
        db.session.commit()
        for author in responce.get('authors'):
            author = requests.get(OPEN_LIBRARY + author.get('key') + '.json').json()
            author = Author(
                key=author.get('key')[9:],
                personal_name=author.get('personal_name'),
                top_work=author.get('top_work')
            )
            author.books.append(book)
            db.session.add(author)
            db.session.commit()
        for work in responce.get('works'):
            work = requests.get(OPEN_LIBRARY + work.get('key') + '.json').json()
            work = Work(
                key=work.get('key')[7:],
                title=work.get('title'),
                book_key=responce.get('key')[7:]
            )
            db.session.add(work)
            db.session.commit()
    books = Book.query.all()
    return jsonify([book.to_json() for book in books])

@app.route("/book/<string:key>", methods=["GET"])
def get_book(key):
    print(key)
    book = Book.query.get(key)
    if book is None:
        abort(404, 'make sure you use book/favourites first!')
    return jsonify(book.to_json())

@app.route("/book/<string:key>", methods=["DELETE"])
def delete_book(key):
    book = Book.query.get(key)
    if book is None:
        abort(404, 'make sure you use book/favourites first!')
    db.session.delete(book)
    db.session.commit()
    return jsonify({'result': True})

@app.route("/book", methods=['POST'])
def create_book():
    if not request.json:
        abort(400,'Failed, please check your request is json')
    book = Book(key=request.json.get('key'),
        title=request.json.get('title'),
        number_of_pages=request.json.get('number_of_pages')
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_json()), 201

@app.route('/book/<string:key>', methods=['PUT'])
def update_book(key):
    if not request.json:
        abort(400)
    book = Book.query.get(key)
    if book is None:
        abort(404,'Not found !')
    book.title = request.json.get('title', book.title)
    book.number_of_pages = request.json.get('number_of_pages', book.number_of_pages)
    db.session.commit()
    return jsonify(book.to_json())
