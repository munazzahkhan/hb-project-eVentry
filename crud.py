""" CRUD operations for eVentry app """

from model import db, User, Theme, Image, Event, EventsItems, Item, Category, connect_to_db


def create_user(fname, lname, email, password):
    """ Create and return a new user """

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_details_by_id(user_id):
    """ Return a user details by user_id """
    
    return User.query.filter(User.user_id == user_id).first()


def get_user_by_email(email):
    """ Return a user by email """

    return User.query.filter(User.email == email).first()


def edit_user_details(user_id, fname, lname):
    """ Edit user details and save them """

    user = get_user_details_by_id(user_id)
    User.query.filter(User.user_id == user_id).update(
        {
            "fname" : fname,
            "lname" : lname,
        }
    )
    db.session.commit()

    return user

def edit_user_password(user_id, password):
    """ Edit user password and save it """

    user = get_user_details_by_id(user_id)
    User.query.filter(User.user_id == user_id).update(
        {
            "password" : password
        }
    )
    db.session.commit()

    return user

def create_theme(color):
    """ Create and return a new theme """

    theme = Theme(color=color)

    db.session.add(theme)
    db.session.commit()

    return theme


def create_image(url):
    """ Create and return a new image """

    image = Image(url=url)
    db.session.add(image)
    db.session.commit()

    return image


def create_category(category):
    """ Create and return a new category """

    category = Category(name=category)
    db.session.add(category)
    db.session.commit()

    return category


def get_categories():
    """ Return all categories """

    return Category.query.all()


def get_category(category):
    """ Return a specific category """

    return Category.query.filter_by(name=category).first()


def create_event(description, user, category, theme, image):
    """ Create and return a new event """

    event = Event(description=description, user_id=user, category_id=category, theme_id=theme, img_id=image)

    db.session.add(event)
    db.session.commit()

    return event


def get_events():
    """ Return all events """

    return Event.query.all()


def get_events_by_category(category):
    """ Return all categories of events """

    return Event.query.filter(Event.category_id==category).all()


def get_events_by_user(user_id):
    """ Return all events by a user """

    return Event.query.filter(Event.user_id==user_id).all()


def is_event_by_user(user_id, event_id):
    """ Return True if the event is by signed in user """

    events = Event.query.filter(Event.user_id==user_id).all()
    for event in events:
        if int(event_id) == int(event.event_id):
            return True

    return False


def get_event_by_id(event_id):
    """ Return the event """

    items_list = EventsItems.query.filter_by(event_id=event_id)
    event = Event.query.filter_by(event_id=event_id).first()

    item_objs = []
    for item in items_list:
        res = Item.query.get(item.item_id)
        item_objs.append(res)

    return (item_objs, event)


def create_events_items(event, item):
    """ Create and return a new event & item relationship """

    event_item = EventsItems(event_id=event, item_id=item)

    db.session.add(event_item)
    db.session.commit()

    return event_item


def create_item(name, description, link, image):
    """ Create and return a new item """

    item = Item(name=name, description=description, link=link, img_id=image)

    db.session.add(item)
    db.session.commit()

    return item


def get_item_by_id(item_id):
    """ Return an item but its id """

    item_id = int(item_id)
    return Item.query.filter(Item.item_id==item_id).first()

def update_item(item_id, name, description, link, img_id):
    """ Edit item details and save them """

    item = Item.query.filter(Item.item_id == item_id).first()
    Item.query.filter(Item.item_id == item_id).update(
        {
            "name" : name,
            "description" : description,
            "link" : link,
            "img_id" : img_id
        }
    )

    db.session.commit()

    return item


if __name__ == '__main__':
    from server import app

    connect_to_db(app)