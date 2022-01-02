from flask import Blueprint, render_template, flash, redirect, url_for, request
from application.users.forms import EditProfileForm, PasswordChangeForm, ChangeEmailForm, \
    DeleteAccountForm
from application.models import User
from application import db
from flask_login import current_user, login_required

users = Blueprint('users', __name__, template_folder='templates')


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
    return render_template('settings_security.html', password_form=password_form,
                           email_form=email_form)


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
