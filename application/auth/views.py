from flask import Blueprint, render_template, flash, redirect, url_for, request
from application.decorators import check_authentication
from application.auth.forms import SignUpForm, SignInForm, ResetPasswordRequestForm, ResetPasswordForm
from application.models import User
from application import db
from flask_login import current_user, login_user, login_required, logout_user
from application.auth.utils import send_email

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/signup', methods=['GET', 'POST'])
@check_authentication
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('main.home'))
    return render_template('sign_up.html', form=form)


@auth.route('/signin', methods=['GET', 'POST'])
@check_authentication
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have signed in as {current_user.username}.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Login unsuccessful. Please check email and password.', 'warning')
        return redirect(url_for('users.sign_in'))
    return render_template('sign_in.html', form=form)


@auth.route('/signout')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('main.home'))


@auth.route('/reset_password_request', methods=['GET', 'POST'])
@check_authentication
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('An email has been sent with instructions to reset your password. Please check «Spam» folder as well.',
              'success')
        return redirect(url_for('auth.sign_in'))
    return render_template('reset_password_request.html', form=form)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
@check_authentication
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token. ', 'warning')
        return redirect(url_for('users.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if form.username.data == user.username:
            user.password = form.password.data
            db.session.commit()
            flash('Your password has been updated! You are now able to sign in.', 'success')
            return redirect(url_for('auth.sign_in'))
        flash('Username is invalid.', 'warning')
        return redirect(request.url)
    return render_template('reset_password.html', form=form)
