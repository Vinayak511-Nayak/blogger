from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('email',validators = [DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('email',validators = [DataRequired(), Email()])
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm_password',message='please verify password')])
    confirm_password = PasswordField('confirm password',validators=[DataRequired()])
    submit = SubmitField('Register')


class BlogForm(FlaskForm):
    title = StringField('Title')
    blog = TextAreaField('Blog')
    submit = SubmitField('Submit')

class AccountForm(FlaskForm):
    username=StringField('Change_username')
    submit= SubmitField('submit')
