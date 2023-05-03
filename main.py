# ------------------------- MODULES ------------------------- #
# imported Flask, render_template, redirect, url_for and request class from flask module
from flask import Flask, render_template, redirect, url_for, request

# imported Bootstrap class from flask_bootstrap module
from flask_bootstrap import Bootstrap

# imported SQLAlchemy class from flask_sqlalchemy module
from flask_sqlalchemy import SQLAlchemy

# imported FlaskForm class from flask_wtf module
from flask_wtf import FlaskForm

# imported StringField, SubmitField and DataRequired class from wtforms module
from wtforms import StringField, SubmitField

# imported DataRequired class
from wtforms.validators import DataRequired

# imported requests module
import requests


# ------------------------- APP CONFIGURATION ------------------------- #
# created instance of Flask class
app = Flask(__name__)

# created instance of Bootstrap class
Bootstrap(app)

# created instance of SQLAlchemy class
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ------------------------- TABLE ------------------------- #
# created Movie table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250))
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

# with app.app_context():
#     db.create_all()

#     def add_movie():
#         new_movie = Movie(title='Phone Booth',
#                            year=2002,
#                            description='Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist\'s sniper rifle. Unable to leave or receive outside help, Stuart\'s negotiation with the caller leads to a jaw-dropping climax.',
#                            rating=7.3,
#                            ranking=10,
#                            review='One of the best movies I\'ve ever seen!',
#                            img_url='https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg'
#                            )

#         db.session.add(new_movie)
#         db.session.commit()

#     add_movie()


# ------------------------- ROUTES ------------------------- #
# route decorator to tell Flask what URL should trigger the function
@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        pass


# ------------------------- MAIN ------------------------- #
# checks if name is equal to main and runs the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
