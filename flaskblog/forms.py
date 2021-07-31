from re import S
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from flaskblog.models import User



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    submit = SubmitField('Log in')



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Me')

    def validate_username(username):
        user = User.query.filter_by(username=username.data)
        if user:
            raise ValidationError('Already is an account with that username. Please choose a different one.')


    def validate_email(email):
        user = User.query.filter_by(email=email.data)
        if user:
            raise ValidationError('Already is an account with that email. Please choose a different one.')




class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[Length(max=30)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    number = IntegerField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Create Contact')



class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[Length(max=30)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    number = IntegerField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Updated Contact')


class ResetRequestForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(),Email()])
        submit = SubmitField('Request password reset')

        def email_validate(email):
            user = User.query.filter_by(email=email.data).first()
            if not user:
                raise ValidationError("There isn't an account with that email.")



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    
