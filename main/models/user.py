import MySQLdb

from main import mysql


class User():
    def change_password(self, email, password):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            f"UPDATE `User` SET `Password`='{password}' WHERE `Email`='{email}'")
        mysql.connection.commit()

        return True

    def create_account(self, email, password):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(f"INSERT INTO `User` VALUES ('{email}', '{password}');")
        mysql.connection.commit()

        return True

    def is_valid_login_creds(self, email, password):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            f"SELECT * FROM user WHERE `Email`='{email}' AND `Password`='{password}'")
        user = cursor.fetchone()

        return user is not None
