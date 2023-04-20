import MySQLdb

from main import mysql


def query_products():
    # Creating a connection cursor
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Executing SQL Statements
    cursor.execute("SELECT * FROM user WHERE `email`='a@q.com'")
    city = cursor.fetchone()

    return city
