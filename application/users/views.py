from flask import Blueprint, render_template, flash, redirect, url_for, request
from application.users.forms import SignUpForm, SignInForm, EditProfileForm, PasswordChangeForm, DeleteAccountForm, \
    ResetPasswordRequestForm, ResetPasswordForm, ChangeEmailForm
from application.models import User
from application import db
from flask_login import current_user, login_user, login_required, logout_user
from application.users.utils import send_email

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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


@users.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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


@users.route('/signout')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


@users.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def settings_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('users.settings_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
    return render_template('settings_profile.html', form=form)


@users.route('/settings/security', methods=['GET', 'POST'])
@login_required
def settings_security():
    password_form = PasswordChangeForm()
    if password_form.validate_on_submit():
        if current_user.verify_password(password_form.password.data):
            current_user.password = password_form.new_password.data
            db.session.commit()
            flash('Your password has been successfully changed.', 'success')
            return redirect(url_for('users.settings_security'))
        flash('Invalid password.', 'warning')
        return redirect(url_for('users.settings_security'))
    email_form = ChangeEmailForm()
    if email_form.validate_on_submit():
        if current_user.verify_password(password_form.password.data):
            current_user.email = email_form.email.data
            db.session.commit()
            flash('Your email has been successfully updated.', 'success')
            return redirect(url_for('users.settings_security'))
        flash('Invalid password.', 'warning')
        return redirect(url_for('users.settings_security'))
    elif request.method == 'GET':
        email_form.email.data = current_user.email
    return render_template('settings_security.html', password_form=password_form, email_form=email_form)


@users.route('/settings/delete', methods=['GET', 'POST'])
@login_required
def account_delete():
    form = DeleteAccountForm()
    confirm_txt = f'{current_user.username}/delete'
    if form.validate_on_submit():
        if form.message.data == confirm_txt and current_user.verify_password(form.password.data):
            db.session.delete(current_user)
            db.session.commit()
            flash('Your account has been deleted.', 'success')
            return redirect(url_for('main.home'))
        flash('Invalid information.', 'warning')
        return redirect(url_for('users.account_delete'))
    return render_template('settings_delete.html', form=form, confirm_txt=confirm_txt)


@users.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('An email has been sent with instructions to reset your password. Please check «Spam» folder as well.',
              'success')
        return redirect(url_for('users.sign_in'))
    return render_template('reset_password_request.html', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
            return redirect(url_for('users.sign_in'))
        flash('Username is invalid.', 'warning')
        return redirect(request.url)
    return render_template('reset_password.html', form=form)
