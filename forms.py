from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired,Email

class RegistrationForm(FlaskForm):
    """Form for new users to register"""
    username = StringField("UserName",[DataRequired()])

    password = PasswordField("Password",[DataRequired()])

    email = StringField("Email",[DataRequired(),Email()])
    
    first_name = StringField("First Name",[DataRequired()])

    last_name = StringField("Last Name",[DataRequired()])


class LoginForm(FlaskForm):
    """Form for exisiting users to log in"""
    username = StringField("UserName",[DataRequired()])

    password = PasswordField("Password",[DataRequired()])

class FeedBackForm(FlaskForm):
    """A form representing feedback"""
    title = StringField("Title",[DataRequired()])

    content = TextAreaField("Content",[DataRequired()])