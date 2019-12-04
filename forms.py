import datetime

from flask_wtf import FlaskForm
#from flask_wtf.file import FileField
from wtforms import StringField, SelectField, TextAreaField, SubmitField, DateTimeField
#from wtforms.fields import BooleanField
#from wtforms.fields.html5 import TimeField
from wtforms.validators import *

# DateField from wtforms_components supports min/max depending on DateRange
from wtforms_components import DateField
#from wtforms_components import DateRange


class LoginForm(FlaskForm):
    login = StringField('Email', validators=[DataRequired(), Email(message='Please enter valid emailaddress')])


class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    due_date = DateField('Due date')
    priority = SelectField('Priority', choices={(0, 'low'), (1, 'mid'), (2, 'high')}, coerce=int, default=1)

    comment = TextAreaField('Comment')

    ''' Zukunftsmusik ..
    parent = SelectField('Parent')
    dependson = SelectField('Depends on')
    '''