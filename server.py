"""Server for eVentry app."""

import os
import urllib.request
from flask import Flask, render_template, request, flash, session, redirect, url_for
from jinja2 import StrictUndefined
from werkzeug.utils import secure_filename
from model import connect_to_db
import crud

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "dev"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.jinja_env.undefined = StrictUndefined


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@app.route('/')
def homepage():
    """ View homepage """

    categories = crud.get_categories()

    return render_template('homepage.html', categories=categories)


@app.route('/sign-in-page')
def show_signin_page_to_user():
    """ Show sign in page to the user """

    return render_template('sign-in.html')


@app.route('/sign-in')
def signin_user():
    """ Sign in an existing user """

    email = request.args.get('email')
    password = request.args.get('password')

    user = crud.get_user_by_email(email)

    # if not user:
    #     flash("No such email address.")
    #     return redirect('/sign-in')

    # if user.password != password:
    #     flash("Incorrect password.")
    #     return redirect('/sign-in')

    # session["signed_in_user_email"] = user.email
    # flash("Logged in.")

    # return redirect('/')

    if user:
        if user.email == email and user.password == password:
            session["signed_in_user_email"] = user.email
            session["signed_in_user_id"] = user.user_id
            flash('Signed in!')
        return redirect('/')
    else:
        flash('Account does not exist.')
        return render_template('sign-in.html')


@app.route("/sign-out")
def signout_user():
    """ Sign out user """

    del session["signed_in_user_email"]
    del session["signed_in_user_id"]
    flash("Logged out.")
    return redirect('/')

@app.route('/sign-up-page')
def show_signup_page_to_user():
    """ Show sign up page to the user """

    return render_template('sign-up.html')


@app.route('/users', methods=['POST'])
def register_user():
    """ Create a new user """


    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('That email is already in use. Try again.')
        return render_template('sign-up.html')
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
    print("*"*30)
    print('event: ', event)
    print("*"*30)
 
    return render_template('event_details.html', event=event, items=items)


@app.route('/view-user-events')
def show_events_by_user():

    user_id = session["signed_in_user_id"]
    events = crud.get_events_by_user(user_id)

    return render_template('all_events.html', events=events)

@app.route('/new-event-page')
def show_new_event_page_to_user():
    """ Show new event page to the user """

    categories = crud.get_categories()

    return render_template('new_event.html', categories=categories)


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

def upload_image(file_name):
    if file_name not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files[file_name]
    if file.filename == '':
        print()
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # flash('Image successfully uploaded')
        return filename
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

def create_new_item(i, file_name):
    """ Create new item from user input """

    name = request.form.get(f'name-{i}')
    description = request.form.get(f'description-{i}')
    link = request.form.get(f'link-{i}')
    image = upload_image(file_name)
    item_image = crud.create_image(f'/{UPLOAD_FOLDER}{image}')
    img_id = item_image.img_id
    
    item = crud.create_item(name, description, link, img_id)

    return item


def create_new_event(file_name):
    """ Create new event from user input """

    category_id = request.form.get('category')
    color = request.form.get('theme')
    image = upload_image(file_name)
    event_image = crud.create_image(f'/{UPLOAD_FOLDER}{image}')
    img_id = event_image.img_id
    user_id = session["signed_in_user_id"]
    theme = crud.create_theme(color)
    theme_id = theme.theme_id
    event = crud.create_event(user_id, category_id, theme_id, img_id)

    return event


@app.route('/new-event', methods=['POST'])
def new_event():
    """ Create a new event with items in it """
    
    number_of_items = int(request.form.get('number-of-items'))
    # image_list = upload_image(number_of_items)
    event = create_new_event('file') 
    i = 0
    while i < number_of_items:
        item = create_new_item(i, f'file-{i}')
        crud.create_events_items(event.event_id, item.item_id)
        i += 1
    events = crud.get_events_by_category(event.category_id)

    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)