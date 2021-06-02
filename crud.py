""" CRUD operations for eVentry app """

from model import db, User, Theme, Image, Event, EventsItems, Item, connect_to_db


def create_user(fname, lname, email, password):
    """ Create and return a new user """

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


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


def create_event(user, category, theme, image):
    """ Create and return a new event """

    event = Event(user=user, category=category, theme=theme, image=image)

    db.session.add(event)
    db.session.commit()

    return event


def create_events_items(event, item):
    """ Create and return a new event item relation """

    event_item = EventsItems(event=event, item=item)

    db.session.add(event_item)
    db.session.commit()

    return event_item


def create_item(description, link, image):
    """ Create and return a new item """

    item = Item(description=description, link=link, image=image)

    db.session.add(item)
    db.session.commit()

    return item


if __name__ == '__main__':
    from server import app

    connect_to_db(app)