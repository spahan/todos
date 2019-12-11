from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms_components import DateField


class LoginForm(FlaskForm):
    login = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Please enter valid emailaddress")],
    )


class TodoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])

    due_date = DateField("Due date")
    priority = SelectField(
        "Priority", choices={(0, "low"), (1, "mid"), (2, "high")}, coerce=int, default=1
    )

    comment = TextAreaField("Comment")

    """ Zukunftsmusik ..
    parent = SelectField('Parent')
    dependson = SelectField('Depends on')
    """
