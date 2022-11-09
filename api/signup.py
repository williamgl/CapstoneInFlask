import mysql.connector


def signup(username, password):
    """
    Creates a new user object in quiz database in RDS
    """
    my_db = mysql.connector.connect(
        host="quiz.c8sslkipdbis.us-west-2.rds.amazonaws.com",
        user="admin",
        password="database1",
        database="quiz"
    )

    cursor = my_db.cursor()

    cursor.execute("SELECT username FROM users;")
    for fetched_name in cursor.fetchall():
        if username in fetched_name:
            cursor.close()
            my_db.close()
            return {"success": "name taken"}

    cursor.close()
    cursor = my_db.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES ('%s', '%s');" % (username, password))
        my_db.commit()
        success = True
    except:
        success = False

    cursor.close()
    my_db.close()

    return {"success": success}


if __name__ == "__main__":
    print(signup("progress_video_test", "654321"))
