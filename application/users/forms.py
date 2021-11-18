from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Email
from application.models import User
from flask_login import current_user


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
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is invalid or taken, please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is invalid or taken, please choose another.')


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign In')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=32),
                                                   Regexp('[A-Za-z0-9_.]*$', 0,
                                                          'Only letters (a-z, A-Z), numbers (0-9), periods (.) and underscores (_) are allowed.'
                                                          )
                                                   ])
    about = TextAreaField('About me', validators=[Length(min=0, max=256)])
    submit = SubmitField('Confirm Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')


class PasswordChangeForm(FlaskForm):
    password = PasswordField('Your Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8),
                                                             Regexp('[A-Za-z0-9_.]*$', 0,
                                                                    'Only letters (a-z, A-Z), numbers (0-9), periods (.) and underscores (_) are allowed.'
                                                                    )
                                                             ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class ChangeEmailForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    submit = SubmitField('Change Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is invalid or taken, please choose another.')


class DeleteAccountForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Delete Account')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
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
