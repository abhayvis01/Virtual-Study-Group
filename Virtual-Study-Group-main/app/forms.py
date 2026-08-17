from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, ValidationError
from app.services.mongo_service import User

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email', validators=[
        DataRequired(), 
        Regexp(EMAIL_REGEX, message="Please enter a valid email address.")
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.get_by_username(username.data.strip())
        if user:
            raise ValidationError('This username is already taken. Please choose another.')

    def validate_email(self, email):
        user = User.get_by_email(email.data.strip().lower())
        if user:
            raise ValidationError('This email is already registered. Please login instead.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class GroupForm(FlaskForm):
    name = StringField('Study Group Name', validators=[DataRequired(), Length(min=3, max=100)])
    category = SelectField('Subject Category', choices=[
        ('Computer Science', 'Computer Science & IT'),
        ('Mathematics', 'Mathematics & Logic'),
        ('Engineering', 'Engineering & Physics'),
        ('Medicine', 'Medicine & Life Sciences'),
        ('Business', 'Business & Economics'),
        ('General', 'General Study Group')
    ], validators=[DataRequired()])
    description = TextAreaField('Description / Objectives', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Create Study Room')


class ResourceForm(FlaskForm):
    name = StringField('Resource Title', validators=[DataRequired(), Length(min=3, max=120)])
    type = SelectField('Resource Type', choices=[
        ('document', 'PDF / Document File'),
        ('note', 'Study Note / Summary'),
        ('link', 'Web Reference / Video Link')
    ], validators=[DataRequired()])
    content = TextAreaField('Description or URL/Note Text', validators=[DataRequired()])
    file = FileField('Upload Attachment (Optional)', validators=[
        FileAllowed(['pdf', 'txt', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'zip'], 'Supported files: PDF, Docs, Images, Zip')
    ])
    submit = SubmitField('Upload Resource')


class JoinRoomForm(FlaskForm):
    room_code = StringField('Enter 6-Character Room Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Join Room')