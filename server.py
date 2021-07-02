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
UPLOAD_FOLDER_PROFILES = 'static/images/profiles/'

app = Flask(__name__)
app.secret_key = "dev"
app.config['UPLOAD_FOLDER_EVENTS'] = UPLOAD_FOLDER_EVENTS
app.config['UPLOAD_FOLDER_ITEMS'] = UPLOAD_FOLDER_ITEMS
app.config['UPLOAD_FOLDER_PROFILES'] = UPLOAD_FOLDER_PROFILES
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ View homepage """

    categories = crud.get_categories()
    events = crud.get_events_in_order_of_most_liked()

    return render_template('homepage.html', categories=categories, events=events)


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
        if user.password == form.password.data:
            session["signed_in_user_id"] = user.user_id
            return redirect('/')
        else:
            flash('Email and password do not match.')
            return redirect('/sign-in-page')
    else:
        flash('Account does not exist.')
        return redirect('/sign-in-page')


@app.route("/sign-out")
def signout_user():
    """ Sign out user """

    del session["signed_in_user_id"]
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
    handle = form.handle.data
    email = form.email.data
    password = form.password.data
    file_name = form.image.name
    image = upload_image(file_name, "profile", form)

    img_id = None
    if image:
        profile_image = crud.create_image(f'/{UPLOAD_FOLDER_PROFILES}{image}')
        img_id = profile_image.img_id

    user_email = crud.get_user_by_email(email)
    user_handle = crud.get_user_by_handle(handle)

    if user_email and user_handle:
        flash('This email and handle are already in use. Try again.')
        return redirect('/sign-up-page')
    elif user_email:
        flash('This email is already in use. Try again.')
        return redirect('/sign-up-page')
    elif user_handle:
        flash('This handle is already in use. Try again.')
        return redirect('/sign-up-page')
    else:
        crud.create_user(fname, lname, handle, email, password, img_id)
        flash('Account created! Please sign in.')

    return redirect('/')


@app.route('/search')
def search():
    """ Search the keyword and return the events/items matching that keyword """

    request.args.get("button")
    keyword = request.args.get("search")
    events = crud.get_events_by_keyword(keyword)
    items = crud.get_items_by_keyword(keyword)
    item_events = {}
    if items:
        for item in items:
            item_objs, item_event = crud.get_event_by_item(item)
            item_events[item] = item_event
    if events or items:
        return render_template('search_results.html', events=events, item_events=item_events)
    else:
        flash("No results mached your search!")
        return redirect("/")


@app.route('/user-profile')
def show_user_profile():
    """ Show profile of the signed in user """

    user_id = session["signed_in_user_id"]
    user = crud.get_user_details_by_id(user_id)
 
    return render_template('user_profile.html', user=user)


@app.route('/edit-profile-page')
def edit_user_profile():
    """ Show edit profile page to the signed in user """

    user_id = session["signed_in_user_id"]
    user = crud.get_user_details_by_id(user_id)
    form = SignupForm(obj=user)
    if request.args.get("edit"):
        return render_template('edit_profile.html', form=form)
    if request.args.get("pw"):
        session["signed_in_user_pw"] = form.password.data
        return render_template('change_password.html', form=form)
    if request.args.get("picture"):
        session["image_type"] = "profile"
        return render_template('edit_image.html', form=form)
    if request.args.get("delete"):
        crud.delete_user(user_id)
        del session["signed_in_user_id"]
        flash("Account deleted")
        return redirect('/')


@app.route('/edit-profile', methods=['GET', 'POST'])
def save_edited_user_profile():
    """ Save edited profile of the signed in user """

    user_id = session["signed_in_user_id"]
    user = crud.get_user_details_by_id(user_id)

    if request.form.get("cancel"):
        return render_template('user_profile.html', user=user)
    if request.form.get("save"):

        form = SignupForm()
        fname = form.fname.data
        lname = form.lname.data
        handle = form.handle.data
        user_handle = crud.get_user_by_handle(handle)
        if user_handle and user.handle != user_handle.handle:
            flash('This handle is already in use. Try again.')
            return render_template('user_profile.html', user=user)
        else:
            user = crud.edit_user_details(user_id, fname, lname, handle)

        return render_template('user_profile.html', user=user)


@app.route('/change-password', methods=['GET', 'POST'])
def save_change_password():
    """ Check old password and then change it to new password """

    user_id = session["signed_in_user_id"]
    if request.form.get("save"):
        old_password = request.form.get("old_pw")
        if old_password == session["signed_in_user_pw"]:
            form = SignupForm()
            password = form.password.data
            user = crud.edit_user_password(user_id, password)
            del session["signed_in_user_pw"]
            return render_template('user_profile.html', user=user)
        else:
            flash("The Old Password is not correct. Please try again.")
            user = crud.get_user_details_by_id(user_id)
            form = SignupForm(obj=user)
            return render_template('change_password.html', form=form)
    if request.form.get("cancel"):
        user = crud.get_user_details_by_id(user_id)
        return render_template('user_profile.html', user=user)


@app.route('/upload-image', methods=['POST'])
def save_new_image():
    """ Uploade a new image """

    user_id = session["signed_in_user_id"]
    if request.form.get("save"):
        form = SignupForm()
        file_name = form.image.name
        if session["image_type"] == "profile":
            image = upload_image(file_name, "profile", form)
            profile_image = crud.create_image(f'/{UPLOAD_FOLDER_PROFILES}{image}')
            img_id = profile_image.img_id
            user = crud.edit_user_profile_picture(user_id, img_id)
            del session["image_type"]
            return render_template('user_profile.html', user=user)
        if session["image_type"] == "event":
            image = upload_image(file_name, "event", form)
            event_image = crud.create_image(f'/{UPLOAD_FOLDER_EVENTS}{image}')
            img_id = event_image.img_id
            event_id = session["event_id"]
            event = crud.edit_event_image(event_id, img_id)
            items, event = crud.get_event_by_id(event_id)
            is_event_by_user = crud.is_event_by_user(user_id, event_id)
            handle = crud.get_handle_for_event(event_id)
            favorite = crud.is_favorite(event_id, user_id)
            like = crud.is_like(event_id, user_id)
            comments = crud.get_all_comments_on_an_event(event_id)
            num_likes = crud.get_likes_of_event(event_id)
            del session["event_id"]
            del session["image_type"]
            return render_template('event_details.html', event=event, 
                                                         items=items, 
                                                         is_event_by_user=is_event_by_user, 
                                                         handle=handle,
                                                         favorite=favorite,
                                                         like=like,
                                                         comments=comments,
                                                         num_likes=num_likes)
        if session["image_type"] == "item":
            image = upload_image(file_name, "item", form)
            item_image = crud.create_image(f'/{UPLOAD_FOLDER_ITEMS}{image}')
            img_id = item_image.img_id
            item_id = session["item_id"]
            event_id = session["event_id"]
            item = crud.edit_item_image(item_id, img_id)
            items, event = crud.get_event_by_id(event_id)
            is_event_by_user = crud.is_event_by_user(user_id, event_id)
            handle = crud.get_handle_for_event(event_id)
            favorite = crud.is_favorite(event_id, user_id)
            like = crud.is_like(event_id, user_id)
            comments = crud.get_all_comments_on_an_event(event_id)
            num_likes = crud.get_likes_of_event(event_id)
            del session["item_id"]
            del session["event_id"]
            del session["image_type"]
            return render_template('event_details.html', event=event, 
                                                         items=items, 
                                                         is_event_by_user=is_event_by_user, 
                                                         handle=handle,
                                                         favorite=favorite,
                                                         like=like,
                                                         comments=comments,
                                                         num_likes=num_likes)
    if request.form.get("cancel"):
        if session["image_type"] == "profile":
            user = crud.get_user_details_by_id(user_id)
            del session["image_type"]
            return render_template('user_profile.html', user=user)
        if session["image_type"] == "event" or session["image_type"] == "item":
            event_id = session["event_id"]
            items, event = crud.get_event_by_id(event_id)
            is_event_by_user = crud.is_event_by_user(user_id, event_id)
            handle = crud.get_handle_for_event(event_id)
            favorite = crud.is_favorite(event_id, user_id)
            like = crud.is_like(event_id, user_id)
            comments = crud.get_all_comments_on_an_event(event_id)
            num_likes = crud.get_likes_of_event(event_id)
            if "item_id" in session:
                del session["item_id"]
            del session["event_id"]
            del session["image_type"]
            return render_template('event_details.html', event=event, 
                                                         items=items, 
                                                         is_event_by_user=is_event_by_user, 
                                                         handle=handle,
                                                         favorite=favorite,
                                                         like=like,
                                                         comments=comments,
                                                         num_likes=num_likes)


@app.route('/events/<category>')
def show_event_category(category):
    """ Show categories of events """

    category = crud.get_category(category)
    events = crud.get_events_by_category(category.category_id)
 
    return render_template('all_events.html', events=events, category=category)


@app.route('/events/<category>/<event_id>', methods=['GET', 'POST'])
def show_event_details(category, event_id):
    """ Show event details """

    if is_user_signed_in():
        user_id = session["signed_in_user_id"]
        if request.form.get("add_comment"):
            comment = request.form.get("comment")
            user_id = session["signed_in_user_id"]
            crud.create_comment(comment, event_id, user_id)
            return redirect(f"/events/{category}/{event_id}")
        comments = crud.get_all_comments_on_an_event(event_id)
        is_event_by_user = crud.is_event_by_user(user_id, event_id)
        handle = crud.get_handle_for_event(event_id)
        items, event = crud.get_event_by_id(event_id)
        favorite = crud.is_favorite(event_id, user_id)
        like = crud.is_like(event_id, user_id)
        num_likes = crud.get_likes_of_event(event_id)
    
        return render_template('event_details.html', event=event, 
                                                    items=items, 
                                                    is_event_by_user=is_event_by_user, 
                                                    handle=handle,
                                                    favorite=favorite,
                                                    like=like,
                                                    comments=comments,
                                                    num_likes=num_likes)
    else:
        flash("Please sign in/sign up to view the details")

        return redirect("/")


@app.route("/edit-event-page")
def edit_event_details():
    """ Show edit event page to the signed in user """

    event_id = request.args.get("event_id")
    items, event = crud.get_event_by_id(event_id)
    if request.args.get("delete_event"):
        crud.delete_event(event_id)
        flash("Event deleted")
        return redirect('/view-user-events')
    event_form = NewEventForm(obj=event)
    event_form.event_description.process_data(event.description)
    if request.args.get("description"):
        return render_template('edit_event.html', form=event_form, event_id=event_id)
    if request.args.get("edit_event_image"):
        session["event_id"] = event_id
        session["image_type"] = "event"
        return render_template('edit_image.html', form=event_form)
    if request.args.get("add"):
        session["new_event_category"] = event_form.category.name
        session["new_event_id"] = event_id
        session["item-added"] = 1
        item_form = NewItemForm()
        return render_template('new_item.html', event_id=event_id, item_form=item_form)
    item_id = request.args.get("item_id")
    item = crud.get_item_by_id(item_id)
    item_form = NewItemForm(obj=item)
    item_form.item_description.process_data(item.description)
    if request.args.get("item"):
        return render_template('edit_item.html', form=item_form, item_id=item_id, event_id=event_id)
    if request.args.get("edit_item_image"):
        session["event_id"] = event_id
        session["item_id"] = item_id
        session["image_type"] = "item"
        return render_template('edit_image.html', form=item_form)
    if request.args.get("delete_item"):
        if len(items) == 1:
            flash("Sorry you cannot delete this item. There should be atleast 1 item in an event.")
        else:
            crud.delete_item(item_id)
            flash("Item deleted")
        user_id = session["signed_in_user_id"]
        items, event = crud.get_event_by_id(event_id)
        is_event_by_user = crud.is_event_by_user(user_id, event_id)
        handle = crud.get_handle_for_event(event_id)
        favorite = crud.is_favorite(event_id, user_id)
        like = crud.is_like(event_id, user_id)
        num_likes = crud.get_likes_of_event(event_id)
        comments = crud.get_all_comments_on_an_event(event_id)
        return render_template('event_details.html', event=event, 
                                                     items=items, 
                                                     is_event_by_user=is_event_by_user, 
                                                     handle=handle,
                                                     favorite=favorite,
                                                     like=like,
                                                     comments=comments, 
                                                     num_likes=num_likes)


@app.route("/edit-item", methods=['POST'])
def edit_item_details():
    """ Save changes made by the signed in user """

    event_id = request.form.get("event_id")
    if request.form.get("save"):
        form = NewItemForm()
        name = form.name.data
        description = form.item_description.data
        link = form.link.data
        item_id = request.form.get("item_id")
        # event_id = request.form.get("event_id")
        item = crud.update_item(item_id, name, description, link)

    user_id = session["signed_in_user_id"]
    is_event_by_user = crud.is_event_by_user(user_id, event_id)
    handle = crud.get_handle_for_event(event_id)
    items, event = crud.get_event_by_id(event_id)
    favorite = crud.is_favorite(event_id, user_id)
    like = crud.is_like(event_id, user_id)
    comments = crud.get_all_comments_on_an_event(event_id)
    num_likes = crud.get_likes_of_event(event_id)
    
    return render_template('event_details.html', event=event, 
                                                 items=items, 
                                                 is_event_by_user=is_event_by_user, 
                                                 handle=handle,
                                                 favorite=favorite,
                                                 like=like,
                                                 comments=comments,
                                                 num_likes=num_likes)


@app.route("/edit-event", methods=['POST'])
def edit_event_description():
    """ Save changes made by the signed in user """

    form = NewEventForm()
    description = form.event_description.data
    event_id = request.form.get("event_id")
    event = crud.update_event(event_id, description)
    user_id = session["signed_in_user_id"]
    is_event_by_user = crud.is_event_by_user(user_id, event_id)
    handle = crud.get_handle_for_event(event_id)
    items, event = crud.get_event_by_id(event_id)
    favorite = crud.is_favorite(event_id, user_id)
    like = crud.is_like(event_id, user_id)
    comments = crud.get_all_comments_on_an_event(event_id)
    num_likes = crud.get_likes_of_event(event_id)
 
    return render_template('event_details.html', event=event, 
                                                 items=items, 
                                                 is_event_by_user=is_event_by_user, 
                                                 handle=handle, 
                                                 favorite=favorite,
                                                 like=like,
                                                 comments=comments,
                                                 num_likes=num_likes)


@app.route('/view-user-events')
def show_events_by_user():
    """ Show events by a user """

    user_id = session["signed_in_user_id"]
    events = crud.get_events_by_user(user_id)

    return render_template('all_events.html', events=events)


@app.route('/view-user-favorites')
def show_favorites_by_user():
    """ Show favorite events by a user """

    user_id = session["signed_in_user_id"]
    events = crud.get_favorite_events_by_user(user_id)
    if not events:
        flash("Your 'Favorite' list is empty")

    return render_template('all_events.html', events=events)


@app.route('/<event_id>/favorite')
def favorite_an_event(event_id):
    """ Favorite/unfavorite this event """

    user_id = session["signed_in_user_id"]
    if crud.is_favorite(event_id, user_id):
        crud.remove_favorite(event_id, user_id)
    else: 
        crud.create_favorite(event_id, user_id)
    items, event = crud.get_event_by_id(event_id)
    is_event_by_user = crud.is_event_by_user(user_id, event_id)
    handle = crud.get_handle_for_event(event_id)
    favorite = crud.is_favorite(event_id, user_id)
    like = crud.is_like(event_id, user_id)
    comments = crud.get_all_comments_on_an_event(event_id)
    num_likes = crud.get_likes_of_event(event_id)
 
    return render_template('event_details.html', event=event, 
                                                 items=items, 
                                                 is_event_by_user=is_event_by_user, 
                                                 handle=handle, 
                                                 favorite=favorite,
                                                 like=like,
                                                 comments=comments, 
                                                 num_likes=num_likes)


@app.route('/<event_id>/like')
def like_an_event(event_id):
    """ Like/unlike this event """

    user_id = session["signed_in_user_id"]
    if crud.is_like(event_id, user_id):
        crud.remove_like(event_id, user_id)
    else: 
        crud.create_like(event_id, user_id)
    items, event = crud.get_event_by_id(event_id)
    is_event_by_user = crud.is_event_by_user(user_id, event_id)
    handle = crud.get_handle_for_event(event_id)
    favorite = crud.is_favorite(event_id, user_id)
    like = crud.is_like(event_id, user_id)
    comments = crud.get_all_comments_on_an_event(event_id)
    num_likes = crud.get_likes_of_event(event_id)
 
    return render_template('event_details.html', event=event, 
                                                 items=items, 
                                                 is_event_by_user=is_event_by_user, 
                                                 handle=handle, 
                                                 favorite=favorite,
                                                 like=like,
                                                 comments=comments,
                                                 num_likes=num_likes)


@app.route('/new-event-page')
def show_new_event_page_to_user():
    """ Show new event page to the user """

    form = NewEventForm()
    categories = crud.get_categories()

    return render_template('new_event.html', categories=categories, form=form)


def upload_image(file_name, type, form):
    """ Get the image from user and upload it """

    if not file_name:
        return None

    file = request.files[file_name]
    if not file or not file.filename:
        return None

    filename = secure_filename(file.filename)
    if type == "item":
        file.save(os.path.join(app.config['UPLOAD_FOLDER_ITEMS'], filename))
    elif type == "event":
        file.save(os.path.join(app.config['UPLOAD_FOLDER_EVENTS'], filename))
    elif type == "profile":
        file.save(os.path.join(app.config['UPLOAD_FOLDER_PROFILES'], filename))
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
        item = create_new_item(item_form.image.name)
        event_id = session["new_event_id"]
        session["item-added"] = 1
        crud.create_events_items(event_id, item.item_id)
        item_form.name.data = ""
        item_form.item_description.data = ""
        item_form.link.data = ""
        return render_template('new_item.html', event_id=event_id, item_form=item_form)
    elif request.form['submit'] == 'Done' or request.form['submit'] == 'Cancel':
        if "item-added" in session:
            event_id = session["new_event_id"]
            category = session["new_event_category"]
            show_event_details(category, event_id)
            del session["new_event_id"]
            del session["new_event_category"]
            del session["item-added"]
            return redirect(f'/events/{category}/{event_id}')
        else:
            flash("Please add atleast 1 item")
            event_id = session["new_event_id"]
            item_form = NewItemForm()
            return render_template('new_item.html', event_id=event_id, item_form=item_form)

@app.route('/new-event', methods=['POST'])
def new_event():
    """ Add a new event with user input """
    
    if request.form.get("add"):
        event_form = NewEventForm()
        event = create_new_event(event_form.image.name) 
        session["new_event_id"] = event.event_id
        session["new_event_category"] = event_form.category.name
        item_form = NewItemForm()

        return render_template('new_item.html', item_form=item_form)
    if request.form.get("cancel"):
        return redirect("/view-user-events")


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)