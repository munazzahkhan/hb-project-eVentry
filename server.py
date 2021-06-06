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

    if user:
        if user.email == email and user.password == password:
            flash('Signed in!')
        return redirect('/')
    else:
        flash('Account does not exist.')
        return render_template('sign-in.html')


@app.route('/sign-up-page')
def show_signup_page_to_user():
    """ Show sign up page to the user """

    return render_template('sign-up.html')


@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""


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

    # print("*"*20)
    # print("in server: events = ", events)
    # print("*"*20)
 
    return render_template('all_events.html', events=events, category=category)


@app.route('/events/<category>/<event_id>')
def show_event_details(category, event_id):
    """ Show event details """

    event = crud.get_event_by_id(category, event_id)

    print("*"*20)
    print("in server: events = ", event)
    print("*"*20)
 
    return render_template('event_details.html', event=event)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)