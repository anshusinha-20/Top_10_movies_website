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
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

with app.app_context():
    db.create_all()


# ------------------------- FORMS ------------------------- #
# created Rate_Movie_Form class
class Rate_Movie_Form(FlaskForm):
    rating = StringField(label='Your rating out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField(label='Your review', validators=[DataRequired()])
    submit = SubmitField(label='Done')

# created Add_Movie_Form class
class Add_Movie_Form(FlaskForm):
    title = StringField(label='Movie title', validators=[DataRequired()])
    submit = SubmitField(label='Add movie')


# ------------------------- API ------------------------- #
# created API_KEY variable
API_KEY = 'your api key'

# created API_URL variables
MOVIE_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


# ------------------------- ROUTES ------------------------- #
# route decorator to tell Flask to run the function below when the '/' page is requested
@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)

# route decorator to tell Flask to run the function below when the '/edit' page is requested
@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = Rate_Movie_Form()
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form)

# route decorator to tell Flask to run the function below when the '/delete' page is requested
@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

# route decorator to tell Flask to run the function below when the '/add' page is requested
@app.route("/add", methods=["GET", "POST"])
def add():
    form = Add_Movie_Form()
    if form.validate_on_submit():
        movie = form.title.data
        # created parameters dictionary
        parameters = {
            'api_key': API_KEY,
            'query': movie
        }

        # created response variable
        response = requests.get(url=MOVIE_SEARCH_URL, params=parameters)
        response.raise_for_status()

        # created movies variable
        movies = response.json()['results']

        return render_template('select.html', movies=movies)
    return render_template('add.html', form=form)

# route decorator to tell Flask to run the function below when the '/find' page is requested
@app.route('/find')
def find():
    movie_id = request.args.get('id')
    if movie_id:
        # created parameters dictionary
        parameters = {
            'api_key': API_KEY,
            'language': 'en-US'
        }

        # created response variable
        response = requests.get(url=f'{MOVIE_INFO_URL}/{movie_id}', params=parameters)
        response.raise_for_status()

        # created data variable
        data = response.json()

        # created new_movie variable
        new_movie = Movie(
            title=data['title'],
            year=data['release_date'].split('-')[0],
            img_url=f'{MOVIE_IMAGE_URL}/{data["poster_path"]}',
            description=data['overview']
        )

        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit', id=new_movie.id))
    

# ------------------------- MAIN ------------------------- #
# checks if name is equal to main and runs the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
