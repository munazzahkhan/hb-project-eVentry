"""Server for eVentry app."""

from flask import Flask, render_template, request, flash, session, redirect
from jinja2 import StrictUndefined
from model import connect_to_db
import crud


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


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

    print("*"*20)
    print("in server: email = ", request.args.get('email'))
    print("in server: password = ", password)
    print("*"*20)

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

    event = crud.get_event_by_id(event_id)

    # print("*"*20)
    # print("in server: events = ", event)
    # print("*"*20)
 
    return render_template('event_details.html', event=event)


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


@app.route('/new-event', methods=['POST'])
def new_event():
    """ Create a new event """

    category_id = request.form.get('category')
    print("*"*20)
    print("in server: category_id = ", category_id)
    print("*"*20)

    color = request.form.get('theme')
    name = request.form.get('name')
    description = request.form.get('description')
    link = request.form.get('link')
    item_image = crud.create_image('/static/images/item-2.jpeg')
    img_id = item_image.img_id
    theme = crud.create_theme(color)
    theme_id = theme.theme_id
    item = crud.create_item(name, description, link, img_id)

    event_image = crud.create_image('/static/images/event-2.jpeg')
    img_id = event_image.img_id
    user_id = session["signed_in_user_id"]

    # category = crud.create_category(category_name)
    # category_id = category_id
    event = crud.create_event(user_id, category_id, theme_id, img_id)

    crud.create_events_items(event.event_id, item.item_id)

    events = crud.get_events_by_category(category_id)

    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)