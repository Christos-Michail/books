from . import db

books = db.Table('book_author',
    db.Column('author_key', db.Integer, db.ForeignKey('authors.key'), primary_key=True),
    db.Column('book_key', db.Integer, db.ForeignKey('books.key'), primary_key=True)
)


class Author(db.Model):
    __tablename__ = 'authors'
    key = db.Column(db.String(50), primary_key=True)
    personal_name = db.Column(db.String(100))
    top_work = db.Column(db.String(100))
    books = db.relationship('Book', secondary=books, lazy='subquery',
        backref=db.backref('authors', lazy=True))

    def to_json(self):
        return {
            'key': self.key,
            'personal_name': self.personal_name,
            'top_work': self.top_work
        }

class Book(db.Model):
    __tablename__ = 'books'
    key = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    number_of_pages = db.Column(db.Integer)
    works = db.relationship('Work', backref='books', lazy='dynamic')
    def to_json(self):
        return {
            'key': self.key,
            'title': self.title,
            'number_of_pages': self.number_of_pages
        }

class Work(db.Model):
    __tablename__ = 'works'
    key = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    book_key = db.Column(db.Integer, db.ForeignKey('books.key'), nullable=False)

    def to_json(self):
        return {
            'key': self.key,
            'title': self.title
        }
