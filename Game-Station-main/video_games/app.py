from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

from werkzeug.utils import secure_filename

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video_games.db'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

class Game(db.Model):
    image = db.Column(db.String(200), nullable=True)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.String(1000), nullable=False)
    listed = db.Column(db.String(1000), nullable=False)
    no_reviews = db.Column(db.String(1000), nullable=False)
    genres = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(1000), nullable=False)
    reviews = db.Column(db.String(1000), nullable=False)
    place = db.Column(db.String(1000), nullable=False)
    playing = db.Column(db.String(1000), nullable=False)
    backlogs = db.Column(db.String(1000), nullable=False)
    wishlist = db.Column(db.String(1000), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/collections', methods=['GET'])
def collections():
    games = Game.query.all()
    sort_by = request.args.get('sort_by', 'title')  # Default to 'title' (alphabetical)
    sort_order = request.args.get('sort_order', 'asc')  # Default to ascending

    # Sorting logic
    if sort_by == 'rating':
        sort_column = Game.rating
    elif sort_by == 'release':
        sort_column = Game.release
    else:
        sort_column = Game.title

    # Apply sorting order
    if sort_order == 'desc':
        games = Game.query.order_by(sort_column.desc()).all()
    else:
        games = Game.query.order_by(sort_column.asc()).all()
    return render_template('collections.html', games=games)

@app.route('/add', methods=['POST'])
def add_game():
    new_game = Game(
        title = request.form['title'],
        release = request.form['release'],
        team = request.form['team'],
        rating = request.form['rating'],
        listed = request.form['listed'],
        no_reviews = request.form['no_reviews'],
        genres = request.form['genres'],
        summary = request.form['summary'],
        reviews = request.form['reviews'],
        place = request.form['place'],
        playing = request.form['playing'],
        backlogs = request.form['backlogs'],
        wishlist = request.form['wishlist']

    )
    image_file = request.files['image']
    image_filename = None
    if image_file:
        image_filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image_file.save(image_path)
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('collections'))

@app.route('/add')
def add():
    db.session.commit()
    return render_template('add.html')

# Route: Delete a game
@app.route('/delete/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
    return redirect(url_for('collections'))

# Route: Edit a game
@app.route('/edit/<int:game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    game = Game.query.get(game_id)
    if request.method == 'POST':
        if game:
            game.image = request.form['image']
            game.title = request.form['title']
            game.release = request.form['release']
            game.team = request.form['team']
            game.rating = request.form['rating']
            game.listed = request.form['listed']
            game.no_reviews = request.form['no_reviews']
            game.genres = request.form['genres']
            game.summary = request.form['summary']
            game.reviews = request.form['reviews']
            game.place = request.form['place']
            game.playing = request.form['playing']
            game.backlogs = request.form['backlogs']
            game.wishlist = request.form['wishlist']

            db.session.commit()
        return redirect(url_for('collections'))
    return render_template('edit.html', game=game)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/connect')
def connect():
    return render_template('connect.html')


if __name__ == '__main__':
    app.run(debug=True)
