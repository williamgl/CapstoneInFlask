from flask import Flask, render_template, json, request, flash, redirect, session
import os
from flask_bootstrap import Bootstrap
import mysql.connector

app = Flask(__name__)
Bootstrap(app)


# Use this database to connect AWS RDS
my_db = mysql.connector.connect(
    host="quiz.c8sslkipdbis.us-west-2.rds.amazonaws.com",
    user="admin",
    password="database1",
    database="quiz"
)
app.config['SECRET_KEY'] = 'secret'

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
    return redirect("/index")


@app.route('/index')
def index():
    return render_template("index.j2")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        cur = my_db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username='%s';" % (username, ))
        user = cur.fetchone()
        if userDetails['password'] == user['password']:
            session['login'] = True
            session['username'] = user['username']
            session['user_id'] = user['user_id']
            flash('Welcome ' + session['username'] + '! You have been successfully logged in', 'success')
        else:
            cur.close()
            flash('Password does not match', 'danger')
            return render_template('login.j2')
        cur.close()
        return redirect('/')
    return render_template('login.j2')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = my_db.cursor()

        # check if this username has been taken
        cur.execute("SELECT username FROM users;")
        for fetched_name in cur.fetchall():
            if username in fetched_name:
                cur.close()
                flash('This username has been taken, please try another username', 'danger')
                return redirect('/signup')

        cur.execute("INSERT INTO users(username, password) " 
                    "VALUES('%s', '%s')" % (username, password))

        my_db.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login')

    return render_template("signup.j2")


@app.route('/about')
def about():
    return render_template("about.j2")


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')


@app.route('/create-quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        total_time = request.form['total_time']
        due_date = request.form['due_date']
        cur = my_db.cursor(dictionary=True)

        cur.execute("INSERT INTO quizzes (total_time, due_date) VALUES ('%s', '%s');"
                    % (total_time, due_date))
        my_db.commit()

        cur.execute("SELECT quiz_id FROM quizzes")
        quiz_id = cur.fetchall()[-1]['quiz_id']

        cur.execute("SELECT user_id FROM users WHERE username = '%s'" % (session['username'], ))
        user_id = cur.fetchone()['user_id']
        cur.execute("INSERT INTO users_quizzes (user_id, quiz_id) VALUES (%d, %d);" % (user_id, quiz_id))
        my_db.commit()
        cur.close()
        session['quiz_id'] = quiz_id
        return redirect('/add-question')

    return render_template("create-quiz.j2")


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = request.form['question']
        score = request.form['score']
        question_type_id = request.form['question_type_id']
        choice1 = request.form['choice1']
        choice2 = request.form['choice2']
        choice3 = request.form['choice3']
        choice4 = request.form['choice4']
        answer = request.form['answer']
        cur = my_db.cursor(dictionary=True)

        query1 = "INSERT INTO questions (question, score, question_type_id, " \
                 "answer, choice1, choice2, choice3, choice4) VALUES " \
                 "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        query2 = "INSERT INTO questions (question, score, question_type_id, " \
                 "answer, choice1, choice2) VALUES " \
                 "('%s', '%s', '%s', '%s', '%s', '%s')"
        query3 = "INSERT INTO questions (question, score, question_type_id, answer) VALUES " \
                 "('%s', '%s', '%s', '%s')"
        if question_type_id == "1":
            cur.execute(query1 % (question, score, question_type_id, answer, choice1, choice2, choice3, choice4))
        elif question_type_id == "2":
            cur.execute(query2 % (question, score, question_type_id, answer, choice1, choice2))
        else:
            cur.execute(query3 % (question, score, question_type_id, answer))
        my_db.commit()
        cur.execute("SELECT question_id FROM questions;")
        question_id = cur.fetchall()[-1]['question_id']
        cur.execute("INSERT INTO quizzes_questions (quiz_id, question_id) VALUES (%d, %d);" % (session['quiz_id'], question_id))
        my_db.commit()
        cur.close()
        flash('Question added successfully! Please add another one.', 'success')
        return redirect('/add-question')

    return render_template("add-question.j2")


@app.route('/my-quiz', methods=['GET', 'POST'])
def view_my_quiz():
    if request.method == 'GET':
        cur = my_db.cursor(dictionary=True)
        cur.execute("SELECT user_id FROM users WHERE username = '%s'" % (session['username'], ))
        user_id = cur.fetchone()['user_id']
        cur.execute("SELECT quizzes.quiz_id, total_time, due_date FROM users_quizzes "
                    "INNER JOIN quizzes ON users_quizzes.quiz_id = quizzes.quiz_id "
                    "WHERE user_id='%s';" % (user_id,))
        result = cur.fetchall()
        return render_template('my-quiz.j2', quiz=result)


@app.route("/delete-quiz/<int:quiz_id>")
def delete_quiz(quiz_id):
    query = "DELETE FROM quizzes WHERE quiz_id=%d;"
    cur = my_db.cursor(dictionary=True)
    cur.execute(query % (quiz_id, ))
    my_db.commit()
    cur.close()
    return redirect("/my-quiz")


@app.route("/view-quiz/<int:quiz_id>")
def view_quiz(quiz_id):
    session['quiz_id'] = quiz_id
    cur = my_db.cursor(dictionary=True)
    query = "SELECT questions.question_id, question, score, type_name, answer, choice1, choice2, choice3, choice4 " \
            "FROM questions INNER JOIN question_types ON questions.question_type_id=question_types.type_id " \
            "INNER JOIN quizzes_questions ON quizzes_questions.question_id=questions.question_id " \
            "WHERE quiz_id=%d;"
    cur.execute(query % (quiz_id, ))
    result = cur.fetchall()
    cur.close()
    return render_template("view-quiz.j2", questions=result)


@app.route("/delete-question/<int:question_id>")
def delete_question(question_id):
    query = "DELETE FROM questions WHERE question_id=%d;"
    cur = my_db.cursor(dictionary=True)
    cur.execute(query % (question_id, ))
    my_db.commit()
    cur.close()
    return redirect("/view-quiz/%s" % (session['quiz_id'],))


"""
@app.route('/test')
def test():
    return render_template("template.j2")
"""

# Listener
if __name__ == "__main__":
    # Start the app on port 28571, it will be different once hosted
    app.run(port=28572, debug=True)
