from flask import Flask, render_template, request
import pymysql
import re
import os
#from flask_mysqldb import MySQL

def sql_connector():
    conn = pymysql.connect(user='root', password='HOney@123', db='ecommerce', host='localhost')
    c = conn.cursor()
    return conn, c


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    conn, c = sql_connector()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        c.execute('SELECT * FROM person WHERE username = %s AND password = %s', (username, password,))

        # Fetch one record and return result
        account = c.fetchone()
        print(account)
        if account:
            print("logged in!!!!!!!")
    c.execute("SELECT * FROM person")
    fetchdata = c.fetchall()
    conn.commit()
    conn.close()
    c.close()
    return render_template('loginpage.html',data=fetchdata)
@app.route('/home',methods=['GET','POST'])
def main():
    return render_template('Home.html')
@app.route('/payment',methods=['GET','POST'])
def payment():
    return render_template('payment.hml')
@app.route('/create',methods=['GET','POST'])
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fname = request.form['fname']
        lname = request.form['lname']
        phonenumber = request.form['phonenumber']
        ssn = request.form['ssn']
        usertype = request.form['usertype']
        dob = request.form['dob']
        gender = request.form['gender']
        password = request.form['password']

        # Check if account exists using MySQL
        conn, c = sql_connector()
        c.execute('SELECT * FROM person WHERE SSN = %s', (ssn))
        account = c.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        # elif not username or not password or not email:
        #     msg = 'Please fill out the form!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('create.html', msg=msg)
if __name__ == '__main__':
    app.run(debug=True)

# pymysql, mysql-connector, mysql-connector-python