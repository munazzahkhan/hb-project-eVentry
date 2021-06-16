from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, validators
import email_validator
from flask_wtf.file import FileField, FileRequired, FileAllowed


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


class SigninForm(FlaskForm):
    email = StringField(
        "Email", 
        validators=[validators.DataRequired(), validators.Email()]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired(), validators.Length(min=4, max=30)]
    )


class SignupForm(FlaskForm):
    fname = StringField(
        "First Name", 
        validators=[validators.DataRequired(), validators.Length(min=2, max=30)]
    )
    lname = StringField(
        "Last Name", 
        validators=[validators.DataRequired(), validators.Length(min=2, max=30)]
    )
    email = StringField(
        "Email", 
        validators=[validators.DataRequired(), validators.Email()]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired(), validators.Length(min=4, max=30)]
    )


class NewEventForm(FlaskForm):
    category = SelectField(
        "Event category", 
        validators=[validators.DataRequired()],
        choices=[
            (1, 'Anniversary'),
            (2, 'Baby Shower'),
            (3, 'Birthday'),
            (4, 'Bridal Shower'),
            (5, 'Graduation'),
            (6, 'Halloween'),
            (7, 'Pool Party'),
            (8, 'Wedding Reception'),
            (9, '4th of July')
        ]
    )
    theme = StringField(
        "Event theme color",
        validators=[validators.DataRequired()]
    )
    event_description = TextAreaField(
        "Description of the event",
        validators=[validators.DataRequired()]
    )
    event_image = FileField(
        'Upload an event image', 
        validators=[FileRequired('File was empty!'), 
        FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')]
    )

class NewItemForm(FlaskForm):
    name = StringField(
        "Item Name", 
        validators=[validators.DataRequired()]
    )
    item_description = TextAreaField(
        "Description",
        validators=[validators.DataRequired()]
    )
    item_image = FileField(
        'Upload an item image', 
        validators=[FileRequired('File was empty!'), 
        FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')]
    )
    link = StringField(
        "Link where to get it from"
    )

