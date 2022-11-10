from flask import Flask, render_template, json
import os
from flask_bootstrap import Bootstrap
import mysql.connector

app = Flask(__name__)
Bootstrap(app)

"""
Use this database to connect AWS RDS
my_db = mysql.connector.connect(
    host="quiz.c8sslkipdbis.us-west-2.rds.amazonaws.com",
    user="admin",
    password="database1",
    database="quiz"
)
"""

"""
Use this database to connect your local database
my_db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    database="quiz"
)
"""


# Routes
@app.route('/')
def root():
    return render_template("index.j2")


@app.route('/index')
def index():
    return render_template("index.j2")


@app.route('/login')
def login():
    return render_template("login.j2")


@app.route('/signup')
def signup():
    return render_template("signup.j2")


@app.route('/about')
def about():
    return render_template("about.j2")


@app.route('/layout')
def layout():
    return render_template("layout.j2")


# Listener
if __name__ == "__main__":
    # Start the app on port 28571, it will be different once hosted
    app.run(port=28571, debug=True)
