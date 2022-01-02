from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Email
from application.models import User


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=32),
                                                   Regexp('[A-Za-z0-9_.]*$', 0,
                                                          'Only letters (a-z, A-Z), numbers (0-9), periods (.) and underscores (_) are allowed.'
                                                          )])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8),
                                                     Regexp('[A-Za-z0-9_.]*$', 0,
                                                            'Only letters (a-z, A-Z), numbers (0-9), periods (.) and underscores (_) are allowed.'
                                                            )])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.get_user_by_username(username.data)
        if user:
            raise ValidationError('The username is invalid or taken, please choose another.')

    def validate_email(self, email):
        user = User.get_user_by_email(email.data)
        if user:
            raise ValidationError('The email is invalid or taken, please choose another.')


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')

    def validate_email(self, email):
        user = User.get_user_by_email(email.data)
        if user is None:
            raise ValidationError('The email is invalid.')


class ResetPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8),
                                                         Regexp('[A-Za-z0-9_.]*$', 0,
                                                                'Only letters (a-z, A-Z), numbers (0-9), periods (.) and underscores (_) are allowed.'
                                                                )
                                                         ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
