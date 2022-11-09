import mysql.connector


def login(username, password):
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

    try:
        cursor.execute("SELECT password FROM users WHERE username='%s';" % username)
        if cursor.fetchone()[0] == password:
            success = True
        else:
          success = False
    except:
        success = False

    cursor.close()
    my_db.close()

    return {"success": success}


if __name__ == "__main__":
    print(login("ligan", "123456"))
    print(login("ligan", "12345"))
