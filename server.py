"""Server for eVentry app."""

import os
import urllib.request
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, validators
import email_validator
from flask_wtf.file import FileField, FileRequired, FileAllowed
from jinja2 import StrictUndefined
from werkzeug.utils import secure_filename, validate_arguments
from model import connect_to_db
import crud

UPLOAD_FOLDER_EVENTS = 'static/images/events/'
UPLOAD_FOLDER_ITEMS = 'static/images/items/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "dev"
app.config['UPLOAD_FOLDER_EVENTS'] = UPLOAD_FOLDER_EVENTS
app.config['UPLOAD_FOLDER_ITEMS'] = UPLOAD_FOLDER_ITEMS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.jinja_env.undefined = StrictUndefined


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@app.route('/')
def homepage():
    """ View homepage """

    categories = crud.get_categories()

    return render_template('homepage.html', categories=categories)


def is_user_signed_in():
    """ Check if user is signed in """

    return session.get("signed_in_user_id") is not None


def flash_errors(form):
    """ Flash errors that we get from Flask form  """

    for key, errors in form.errors.items():
        for error in errors:
            flash(f"Error: '{getattr(form, key).label.text}' - {error}", "error")


class SigninForm(FlaskForm):
    email = StringField(
        "Email", 
        validators=[validators.DataRequired(), validators.Email()]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired(), validators.Length(min=4, max=30)]
    )


@app.route('/sign-in-page')
def show_signin_page_to_user():
    """ Show sign in page to the user """

    form = SigninForm()

    return render_template('sign-in.html', form=form)


# @app.route('/sign-in-page')
# def show_signin_page_to_user():
#     """ Show sign in page to the user """

#     return render_template('sign-in.html')


@app.route('/sign-in', methods=["POST"])
def signin_user():
    """ Sign in an existing user """

    form = SigninForm()
    if not form.validate_on_submit():
        flash_errors(form)
        return redirect('/sign-in-page')

    user = crud.get_user_by_email(form.email.data)

    if user:
        session["signed_in_user_id"] = user.user_id
        flash('Signed in!')
        return redirect('/')
    else:
        flash('Account does not exist.')
        return redirect('/sign-in-page')


# @app.route('/sign-in')
# def signin_user():
#     """ Sign in an existing user """

#     email = request.args.get('email')
#     password = request.args.get('password')

#     user = crud.get_user_by_email(email)

#     # if not user:
#     #     flash("No such email address.")
#     #     return redirect('/sign-in')

#     # if user.password != password:
#     #     flash("Incorrect password.")
#     #     return redirect('/sign-in')

#     # session["signed_in_user_email"] = user.email
#     # flash("Logged in.")

#     # return redirect('/')

#     if user:
#         if user.email == email and user.password == password:
#             session["signed_in_user_email"] = user.email
#             session["signed_in_user_id"] = user.user_id
#             flash('Signed in!')
#         return redirect('/')
#     else:
#         flash('Account does not exist.')
#         return render_template('sign-in.html')


@app.route("/sign-out")
def signout_user():
    """ Sign out user """

    del session["signed_in_user_id"]
    flash("Logged out.")
    return redirect('/')


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



@app.route('/sign-up-page')
def show_signup_page_to_user():
    """ Show sign up page to the user """

    form = SignupForm()

    return render_template('sign-up.html', form=form)


# @app.route('/sign-up-page')
# def show_signup_page_to_user():
#     """ Show sign up page to the user """

#     return render_template('sign-up.html')


@app.route('/sign-up', methods=['POST'])
def register_user():
    """ Create a new user account """

    form = SignupForm()
    if not form.validate_on_submit():
        flash_errors(form)
        return redirect('/sign-up-page')

    fname = form.fname.data
    lname = form.lname.data
    email = form.email.data
    password = form.password.data

    user = crud.get_user_by_email(email)
    if user:
        flash('This email is already in use. Try again.')
        return redirect('/sign-up-page')
    else:
        crud.create_user(fname, lname, email, password)
        flash('Account created! Please sign in.')

    return redirect('/')


# @app.route('/sign-up', methods=['POST'])
# def register_user():
#     """ Create a new user """


#     fname = request.form.get('fname')
#     lname = request.form.get('lname')
#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = crud.get_user_by_email(email)
#     if user:
#         flash('That email is already in use. Try again.')
#         return render_template('sign-up.html')
#     else:
#         crud.create_user(fname, lname, email, password)
#         flash('Account created! Please sign in.')

#     return redirect('/')


@app.route('/events/<category>')
def show_event_category(category):
    """ Show categories of events """

    category = crud.get_category(category)
    events = crud.get_events_by_category(category.category_id)
 
    return render_template('all_events.html', events=events, category=category)


@app.route('/events/<category>/<event_id>')
def show_event_details(category, event_id):
    """ Show event details """

    items, event = crud.get_event_by_id(event_id)
 
    return render_template('event_details.html', event=event, items=items)


@app.route('/view-user-events')
def show_events_by_user():

    user_id = session["signed_in_user_id"]
    events = crud.get_events_by_user(user_id)

    return render_template('all_events.html', events=events)

# @app.route('/new-event-page')
# def show_new_event_page_to_user():
#     """ Show new event page to the user """

#     categories = crud.get_categories()

#     return render_template('new_event.html', categories=categories)


# def upload_image(i):
#     """ Upload image taken as input from user """

#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     files = request.files.getlist('file')
#     j = 0
#     while j < i:
#         files.append(request.files[f'file-{j}'])
#         j += 1
#     print("*"*30)
#     print('files: ', files)
#     print("*"*30)
#     file_names = []
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_names.append(filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         else:
#             print("*"*30)
#             print('file_names: ', file_names)
#             print("*"*30)
#             flash('Allowed image types are -> png, jpg, jpeg, gif')
#             return redirect(request.url)

#     return file_names


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


@app.route('/new-event-page')
def show_new_event_page_to_user():
    """ Show new event page to the user """

    form = NewEventForm()
    categories = crud.get_categories()

    return render_template('new_event.html', categories=categories, form=form)



# def upload_image(file_name, type, form):
#     if file_name not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files[file_name]
#     if file.filename == '':
#         print()
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         if type == "item":
#             file.save(os.path.join(app.config['UPLOAD_FOLDER_ITEMS'], filename))
#         elif type == "event":
#             file.save(os.path.join(app.config['UPLOAD_FOLDER_EVENTS'], filename))
#         # flash('Image successfully uploaded')
#         return filename
#     else:
#         flash('Allowed image types are -> png, jpg, jpeg, gif')
#         return redirect(request.url)

def upload_image(file_name, type, form):
    file = request.files[file_name]
    filename = secure_filename(file.filename)
    if type == "item":
        file.save(os.path.join(app.config['UPLOAD_FOLDER_ITEMS'], filename))
    elif type == "event":
        file.save(os.path.join(app.config['UPLOAD_FOLDER_EVENTS'], filename))
    return filename

def create_new_item(file_name):
    """ Create new item from user input """

    form = NewItemForm()
    name = form.name.data
    description = form.item_description.data
    link = form.link.data
    image = upload_image(file_name, "item", form)
    item_image = crud.create_image(f'/{UPLOAD_FOLDER_ITEMS}{image}')
    img_id = item_image.img_id
    
    item = crud.create_item(name, description, link, img_id)

    return item


def create_new_event(file_name):
    """ Create new event from user input """

    form = NewEventForm()
    category_id = form.category.data
    color = form.theme.data
    description = form.event_description.data
    image = upload_image(file_name, "event", form)
    event_image = crud.create_image(f'/{UPLOAD_FOLDER_EVENTS}{image}')
    img_id = event_image.img_id
    user_id = session["signed_in_user_id"]
    theme = crud.create_theme(color)
    theme_id = theme.theme_id
    event = crud.create_event(description, user_id, category_id, theme_id, img_id)

    return event


@app.route('/add-item', methods=['POST'])
def new_item():
    if request.form['submit'] == 'Add this item':
        item_form = NewItemForm()
        item = create_new_item(item_form.item_image.name)
        event_id = session["new_event_id"]
        crud.create_events_items(event_id, item.item_id)
        item_form.name.data = ""
        item_form.item_description.data = ""
        item_form.link.data = ""
        return render_template('new_item.html', event_id=event_id, item_form=item_form)
    elif request.form['submit'] == 'Done':
        del session["new_event_id"]
        return redirect('/')


@app.route('/new-event', methods=['POST'])
def new_event():
    """ Create a new event with items in it """
    
    event_form = NewEventForm()
    event = create_new_event(event_form.event_image.name) 
    session["new_event_id"] = event.event_id
    item_form = NewItemForm()

    # item_form = NewItemForm()
    # number_of_items = int(request.form.get('number-of-items'))
    
    # i = 0
    # while i < number_of_items:
    #     item = create_new_item(item_form.item_image.name)
    #     crud.create_events_items(event.event_id, item.item_id)
    #     i += 1
    # events = crud.get_events_by_category(event.category_id)

    return render_template('new_item.html', item_form=item_form)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)