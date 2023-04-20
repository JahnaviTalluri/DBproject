from flask import request
from main import app, browse_products, constants, login


@app.route(constants.LOGIN_PAGE, methods=['GET', 'POST'])
def welcome_page():
    if request.method == 'GET':
        return login.login_page(step=None)
    elif request.method == 'POST':
        return login.login_submit(step=None)


@app.route(constants.LOGIN_PAGE_PARAM, methods=['GET', 'POST'])
def login_page(step):
    if request.method == 'GET':
        return login.login_page(step)
    elif request.method == 'POST':
        return login.login_submit(step)


@app.route('/products')
def products():
    return browse_products.query_products()
