from flask_mail import Message
from application import mail
from flask import render_template


def send_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    msg.html = render_template('reset_password_email.html', token=token, user=user)
    mail.send(msg)
