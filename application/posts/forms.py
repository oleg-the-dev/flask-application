from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
