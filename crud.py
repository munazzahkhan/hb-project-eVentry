""" CRUD operations for eVentry app """

from model import db, User, Theme, Image, Event, EventsItems, Item, Category, connect_to_db


def create_user(fname, lname, email, password):
    """ Create and return a new user """

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    """Return a user by email."""
    print(email)
    return User.query.filter(User.email == email).first()


def create_theme(name, color):
    """ Create and return a new theme """

    theme = Theme(name=name, color=color)

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

    category = Category(category=category)
    db.session.add(category)
    db.session.commit()

    return category


def get_categories():
    """ Return all categories """

    return Category.query.all()


def get_category(category):
    """ Return a specific category """

    return Category.query.filter_by(category=category).first()


def create_event(user, category, theme, image):
    """ Create and return a new event """

    event = Event(user_id=user, category_id=category, theme_id=theme, img_id=image)

    db.session.add(event)
    db.session.commit()

    return event


def get_events():
    """ Return all events """

    return Event.query.all()


def get_events_by_category(category):
    """ Return all categories of events """

    return Event.query.filter(Event.category_id==category).all()


def get_event_by_id(category, event_id):
    """ Return the event """

    # event = Event.query.filter_by(category=category)
    items_list = EventsItems.query.filter_by(event_id=event_id)

    item_objs = []
    for item in items_list:
        res = Item.query.get(item.item_id)
        item_objs.append(res)
    print(item_objs)

    return item_objs


def create_events_items(event, item):
    """ Create and return a new event & item relationship """

    event_item = EventsItems(event_id=event, item_id=item)

    db.session.add(event_item)
    db.session.commit()

    return event_item


def create_item(description, link, image):
    """ Create and return a new item """

    item = Item(description=description, link=link, img_id=image)

    db.session.add(item)
    db.session.commit()

    return item


if __name__ == '__main__':
    from server import app

    connect_to_db(app)