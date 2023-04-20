import MySQLdb

from main import mysql


class User():
    def __init__(self, email):
        self.email = email

    def change_password(self, password):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            f"UPDATE `User` SET `Password`='{password}' WHERE `Email`='{self.email}'")
        mysql.connection.commit()

        return True

    def create_account(self, password):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            f"INSERT INTO `User` VALUES ('{self.email}', '{password}');")
        mysql.connection.commit()

        return True

    def is_valid_login_creds(self, password):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            f"SELECT * FROM user WHERE `Email`='{self.email}' AND `Password`='{password}'")
        user = cursor.fetchone()

        return user is not None
