from flask import Flask, render_template, request ,redirect , url_for ,session
import pymysql
import uuid
from random import randint, randrange
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
    msg = ''
    if request.method == 'POST':
        ssn = request.form.get('ssn')
        password = request.form.get('password')
        usertype = request.form.get('usertype')
        print(ssn)
        print(password)
        c.execute(f"SELECT * FROM person as P, {usertype} as C WHERE P.ssn = C.ssn AND P.ssn = {ssn} AND P.password = '{password}';")

        # Fetch one record and return result
        account = c.fetchone()

        print(account)
        if account:
            session['user'] = ssn
            session['usertype'] = usertype
            msg="logged in!!!!!!!"
            return redirect(url_for('main'))
        else:
            msg="wrong credentials"
    c.execute("SELECT * FROM person")
    fetchdata = c.fetchall()
    conn.commit()
    conn.close()
    c.close()
    return render_template('loginpage.html',data=fetchdata, msg=msg)

@app.route('/home',methods=['GET','POST'])
def main():
    ssn = session['user']
    usertype = session['usertype']
    conn, c = sql_connector()
    c.execute('SELECT * FROM person where ssn = %s ', (ssn))
    data1 = c.fetchall()
    print(data1)
    print("----")
    return render_template('Home.html',data=data1, usertype=usertype)

@app.route('/product/<string:view>',methods=['GET','POST'])
def product(view):
    ssn = session['user']
    usertype = session['usertype']

    conn, c = sql_connector()
    msg = ""

    if request.method == 'POST':
        if view == 'create' and 'product_id' in request.form and 'name' in request.form and 'price' in request.form:
            product_id = request.form['product_id']
            name = request.form['name']
            price = request.form['price']

            c.execute('INSERT INTO product VALUES(%s, %s, %s , %s)',(product_id, name, price, ssn))
            conn.commit()

            msg = 'Created Succesfully'
            return redirect(url_for('main'))
        else:
            msg = "Please fill the form!"

    if usertype == 'customer':
        c.execute('SELECT * FROM product ORDER BY CAST(price AS float) ASC')
    elif usertype == 'supplier':
        c.execute(f"SELECT * FROM product WHERE supplier='{ssn}'")

    fetchdata = c.fetchall()
    return render_template('product.html',view=view,products=fetchdata, usertype=usertype, msg=msg, product_info=None)

@app.route('/product/edit/<string:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    usertype = session['usertype']

    conn, c = sql_connector()
    msg = ""

    c.execute(f"SELECT * FROM product WHERE product_id={product_id}")
    product_info = c.fetchone()

    if request.method == 'POST':
        if 'name' in request.form and 'price' in request.form:
            name = request.form['name']
            price = request.form['price']

            c.execute('UPDATE Product SET name=%s, price=%s WHERE product_id=%s;',(name, price, product_id))
            conn.commit()

            msg = 'Updated Succesfully'
            return redirect(url_for('main'))

    return render_template('product.html', view='edit', products=[], usertype=usertype, msg=msg, product_info=product_info)

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/home/product/payment/<string:product_id>',methods=['GET','POST'])
def payment(product_id,ssn):
    print(product_id)
    conn, c = sql_connector()
    c.execute('SELECT * FROM product where Product_ID = %s ',(product_id))
    data1 = c.fetchall()
    print(data1)
    return render_template('payment.html',data=data1)

@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template('contact.html')

@app.route('/home/<string:ssn>/order',methods=['GET','POST'])
def order(ssn):
    conn, c = sql_connector()
    c.execute('SELECT * FROM order1 where cssn = %s ', (ssn))
    data1 = c.fetchall()
    c.execute('select * from order_product1 , product ,order1  where order_product1.Product_ID=product.product_ID and order_product1.orderID=order1.orderID  and cssn = %s',(ssn))
    product=c.fetchall()
    ssn=ssn
    return render_template('order.html',products=data1,dataproduct=product,cssn=ssn)
@app.route('/home/<string:ssn>/product/payment/<string:productid>/ordered',methods=['GET','POST'])
def placeorder(productid,ssn):
        msg=''
        ID = uuid.uuid4()
        Order_ID = str(randrange(100000, 999999))
        print(Order_ID)
        Product_ID = int(productid)
        print("what's wrong", Product_ID)
        ssn = ssn
        status = "placed"
        conn, c = sql_connector()
        c.execute('INSERT INTO order1 VALUES( %s,%s,%s )',(Order_ID,ssn,status) )
        c.execute('INSERT INTO order_product1 VALUES(%s,%s)',(Order_ID,Product_ID))
        conn.commit()
        if c.rowcount == 1:
            msg = 'Order Placedd '
            print("order placedddd")
        else:
            msg = 'Error in the values entered'
            print("not ordereddddd")
        return render_template('orderplaced.html',msg=msg,ssn=ssn)
@app.route('/create',methods=['GET','POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'ssn' in request.form and 'password' in request.form and 'fname' in request.form:
        # Create variables for easy access
        fname = request.form['fname']
        lname = request.form['lname']
        phonenumber = request.form['phonenumber']
        ssn = request.form['ssn']
        usertype = request.form['usertype']
        dob = request.form['dob']
        gender = request.form['gender']
        password = request.form['password']
        print(fname)


        # Check if account exists using MySQL
        conn, c = sql_connector()
        if usertype=="customer":
         c.execute('INSERT INTO person VALUES(%s, %s, %s ,%s ,%s,%s,%s)',(ssn, fname, lname ,gender, phonenumber, dob,password))
         c.execute('INSERT INTO customer values(%s)',(ssn))
         conn.commit()
        # If account exists show error and validation checks
        if c.rowcount==1:
            c.execute(F"INSERT INTO {usertype} VALUES({ssn})")
            conn.commit()

            if c.rowcount == 1:
                msg = 'Registerd Succesfully '
                return redirect(url_for('home', msg=msg))
            else:
                msg='Error in the values entered'
        else:
            msg='Error in the values entered'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address!'
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'Username must contain only characters and numbers!'
        # elif not username or not password or not email:
        #     msg = 'Please fill out the form!'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form!'

    return render_template('create.html', msg=msg)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)

# pymysql, mysql-connector, mysql-connector-python
