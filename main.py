from flask import Flask, render_template, request
import pymysql
#from flask_mysqldb import MySQL

def sql_connector():
    conn = pymysql.connect(user='root', password='HOney@123', db='ecommerce', host='localhost')
    c = conn.cursor()
    return conn, c


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    conn, c = sql_connector()
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
def create():
    return render_template('create.html')
if __name__ == '__main__':
    app.run(debug=True)

# pymysql, mysql-connector, mysql-connector-python