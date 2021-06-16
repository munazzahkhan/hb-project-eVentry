"""Server for eVentry app."""

import os
import urllib.request
from flask import Flask, render_template, request, flash, session, redirect, url_for
from jinja2 import StrictUndefined
from werkzeug.utils import secure_filename, validate_arguments
from form import SigninForm, SignupForm, NewEventForm, NewItemForm
from model import connect_to_db
import crud

UPLOAD_FOLDER_EVENTS = 'static/images/events/'
UPLOAD_FOLDER_ITEMS = 'static/images/items/'

app = Flask(__name__)
app.secret_key = "dev"
app.config['UPLOAD_FOLDER_EVENTS'] = UPLOAD_FOLDER_EVENTS
app.config['UPLOAD_FOLDER_ITEMS'] = UPLOAD_FOLDER_ITEMS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.jinja_env.undefined = StrictUndefined


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


@app.route('/sign-in-page')
def show_signin_page_to_user():
    """ Show sign in page to the user """

    form = SigninForm()

    return render_template('sign-in.html', form=form)


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


@app.route("/sign-out")
def signout_user():
    """ Sign out user """

    del session["signed_in_user_id"]
    flash("Logged out.")
    return redirect('/')


@app.route('/sign-up-page')
def show_signup_page_to_user():
    """ Show sign up page to the user """

    form = SignupForm()

    return render_template('sign-up.html', form=form)


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
    """ Show events by a user """

    user_id = session["signed_in_user_id"]
    events = crud.get_events_by_user(user_id)

    return render_template('all_events.html', events=events)


@app.route('/new-event-page')
def show_new_event_page_to_user():
    """ Show new event page to the user """

    form = NewEventForm()
    categories = crud.get_categories()

    return render_template('new_event.html', categories=categories, form=form)


def upload_image(file_name, type, form):
    """ Get the image from user and upload it """

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
    """ Add new item from user input to the event """

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
        event_id = session["new_event_id"]
        category = session["new_event_category"]
        show_event_details(category, event_id)
        del session["new_event_id"]
        del session["new_event_category"]
        return redirect(f'/events/{category}/{event_id}')


@app.route('/new-event', methods=['POST'])
def new_event():
    """ Add a new event with user input """
    
    event_form = NewEventForm()
    event = create_new_event(event_form.event_image.name) 
    session["new_event_id"] = event.event_id
    session["new_event_category"] = event_form.category.name
    item_form = NewItemForm()

    return render_template('new_item.html', item_form=item_form)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)