from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<BOOK>: {self.title}'



@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', book=all_books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        new_book = Books(title=request.form['title'],
                        author=request.form['author'],
                        rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        book_id = request.form['id']
        book_edit = Books.query.get(book_id)
        book_edit.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))

    book = request.args.get('id')
    current_book = Books.query.get(book)

    return render_template('edit.html', book=current_book)



@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    book_delete = Books.query.get(book_id)
    db.session.delete(book_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
