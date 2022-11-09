import mysql.connector


def create_quiz(username, total_score, total_time, due_date):
    my_db = mysql.connector.connect(
        host="quiz.c8sslkipdbis.us-west-2.rds.amazonaws.com",
        user="admin",
        password="database1",
        database="quiz"
    )

    cursor = my_db.cursor()

    try:
        cursor.execute("INSERT INTO quizzes (total_score, total_time, due_date) VALUES (%d, %d, '%s');"
                       % (total_score, total_time, due_date))
        my_db.commit()

        cursor.execute("SELECT COUNT(quiz_id) FROM quizzes")
        quiz_id = cursor.fetchone()[0]
        user2quiz(username, quiz_id)

        success = True
    except:
        success = False

    cursor.close()
    my_db.close()

    return {"success": success}


def user2quiz(username, quiz_id):
    my_db = mysql.connector.connect(
        host="quiz.c8sslkipdbis.us-west-2.rds.amazonaws.com",
        user="admin",
        password="database1",
        database="quiz"
    )

    cursor = my_db.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = '%s'" % username)
    user_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO users_quizzes (user_id, quiz_id) VALUES (%d, %d);" % (user_id, quiz_id))
    my_db.commit()
    cursor.close()
    my_db.close()


if __name__ == '__main__':
    print(create_quiz('ligan', 100, 60, '2022-12-25'))
