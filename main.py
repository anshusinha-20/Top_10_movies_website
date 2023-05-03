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

# created instance of Flask class
app = Flask(__name__)

# created instance of SQLAlchemy class
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# route decorator to tell Flask what URL should trigger the function
@app.route("/")
def home():
    return render_template("index.html")


# checks if name is equal to main and runs the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
