from flask import redirect, render_template

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields import EmailField
# from wtforms.validators import DataRequired, InputRequired

from main.constants import BROWSE_PRODUCTS_PAGE, EMAIL_SIZE, LOGIN_PAGE, LOGIN_PAGE_EXISTING_USER, LOGIN_PAGE_FORGOT_PASSWORD, LOGIN_PAGE_NEW_USER, PASSWORD_SIZE
from main.models import User


class ExistingUserForm(FlaskForm):
    email = EmailField('Email', render_kw={'size': EMAIL_SIZE}, validators=[])
    password = PasswordField('Password', render_kw={
                             'size': PASSWORD_SIZE}, validators=[])
    login = SubmitField('Login')
    forgot_password = SubmitField('Forgot Password')

    def get_email(self):
        return self.email.data

    def get_password(self):
        return self.password.data

    def handle_form_submitted(self):
        if self.is_login_clicked():
            email_input = self.get_email()
            password_input = self.get_password()

            if email_input and password_input:
                return login_user(self)
        elif self.is_forgot_password_clicked():
            return redirect(LOGIN_PAGE_FORGOT_PASSWORD)

    def is_forgot_password_clicked(self):
        return self.forgot_password.data

    def is_login_clicked(self):
        return self.login.data


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', render_kw={'size': EMAIL_SIZE}, validators=[])
    new_password = PasswordField('New password', render_kw={
                                 'size': PASSWORD_SIZE}, validators=[])
    reset_password = SubmitField('Reset password')

    def get_email(self):
        return self.email.data

    def get_new_password(self):
        return self.new_password.data

    def handle_form_submitted(self):
        if self.is_reset_password_clicked():
            email_input = self.get_email()
            new_password_input = self.get_new_password()

            if email_input and new_password_input:
                return change_user_password(self)

    def is_reset_password_clicked(self):
        return self.reset_password.data


class NewUserForm(FlaskForm):
    email = EmailField('Email', render_kw={'size': EMAIL_SIZE}, validators=[])
    password = PasswordField('Password', render_kw={
                             'size': PASSWORD_SIZE}, validators=[])
    create_account = SubmitField('Create account')

    def get_email(self):
        return self.email.data

    def get_password(self):
        return self.password.data

    def handle_form_submitted(self):
        if self.is_create_account_clicked():
            email_input = self.get_email()
            password_input = self.get_password()

            if email_input and password_input:
                return create_user_account(self)

    def is_create_account_clicked(self):
        return self.create_account.data


class WelcomeForm(FlaskForm):
    login = SubmitField('Login')
    create_account = SubmitField('Create a new account')

    def handle_form_submitted(self):
        if self.is_login_clicked():
            return redirect(LOGIN_PAGE_EXISTING_USER)
        elif self.is_create_account_clicked():
            return redirect(LOGIN_PAGE_NEW_USER)

    def is_create_account_clicked(self):
        return self.create_account.data

    def is_login_clicked(self):
        return self.login.data


def change_user_password(form: ForgotPasswordForm):
    email = form.get_email()
    new_password = form.get_new_password()

    password_changed = User().change_password(email, new_password)

    return redirect(LOGIN_PAGE_EXISTING_USER) if password_changed else None


def create_user_account(form: NewUserForm):
    email = form.get_email()
    password = form.get_password()

    user_created = User().create_account(email, password)

    return redirect(LOGIN_PAGE_EXISTING_USER) if user_created else None


def get_login_form(step):
    form = None

    if step == 'existing_user':
        form = ExistingUserForm()
    elif step == 'forgot_password':
        form = ForgotPasswordForm()
    elif step == 'new_user':
        form = NewUserForm()
    elif step is None:
        form = WelcomeForm()

    return form


def login_page(step):
    form = get_login_form(step)
    return render_template('login.html', step=step, form=form)


def login_submit(step):
    form = get_login_form(step)
    return form.handle_form_submitted()


def login_user(form: ExistingUserForm):
    email = form.get_email()
    password = form.get_password()

    valid_creds = User().is_valid_login_creds(email, password)

    return redirect(BROWSE_PRODUCTS_PAGE) if valid_creds else redirect(LOGIN_PAGE)
