""" CRUD operations for eVentry app """

from sqlalchemy import *
from model import db, User, Theme, Image, Event, EventsItems, Favorite, Like, Item, Comment, Category, connect_to_db


def create_user(fname, lname, handle, email, password, img_id):
    """ Create and return a new user """

    user = User(fname=fname, lname=lname, handle=handle, email=email, password=password, img_id=img_id)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_details_by_id(user_id):
    """ Return a user details by user_id """
    
    return User.query.filter(User.user_id == user_id).first()


def get_user_by_email(email):
    """ Return a user by email """

    return User.query.filter(User.email == email).first()


def get_user_by_handle(handle):
    """ Return a user by handle """

    return User.query.filter(User.handle == handle).first()


def get_handle_by_user_id(user_id):
    """ Return handle of the user """

    user = get_user_details_by_id(user_id)

    return user.handle


def edit_user_details(user_id, fname, lname, handle):
    """ Edit user details and save them """

    user = get_user_details_by_id(user_id)
    User.query.filter(User.user_id == user_id).update(
        {
            "fname" : fname,
            "lname" : lname,
            "handle" : handle
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


def edit_user_profile_picture(user_id, img_id):
    """ Edit user profile picture and save it """

    user = get_user_details_by_id(user_id)
    User.query.filter(User.user_id == user_id).update(
        {
            "img_id" : img_id
        }
    )
    db.session.commit()

    return user


def delete_user(user_id):
    """ Delete user from Users table """

    events = get_events_by_user(user_id)
    if events:
        for event in events:
            delete_event(event.event_id)
    User.query.filter(User.user_id == user_id).delete()
    db.session.commit()


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


def get_events_by_keyword(keyword):
    """ Search by keyword and return all events """

    events = Event.query.filter(Event.description.like(f'%{keyword}%')).all()
    themes = Theme.query.filter(Theme.color.like(f'%{keyword}%')).all()
    for theme in themes:
        event = Event.query.filter(Event.theme_id==theme.theme_id).all()
        events.extend(event)
    
    return events


def get_handle_for_event(event_id):
    """ Return event handle for an event """

    event = Event.query.filter(Event.event_id==event_id).first()
    user_id = event.user_id
    user = get_user_details_by_id(user_id)
    return user.handle


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


def update_event(event_id, description):
    """ Edit event details and save them """

    event = get_event_by_id(event_id)
    Event.query.filter(Event.event_id == event_id).update(
        {
            "description" : description
        }
    )

    db.session.commit()

    return event


def edit_event_image(event_id, img_id):
    """ Edit event image and save it """

    event = get_event_by_id(event_id)
    Event.query.filter(Event.event_id == event_id).update(
        {
            "img_id" : img_id
        }
    )
    db.session.commit()

    return event


def delete_event(event_id):
    """ Delete event from Events table """

    items, event = get_event_by_id(event_id)
    if items:
        for item in items:
            delete_item(item.item_id)
        EventsItems.query.filter(EventsItems.event_id == event_id).delete()
    Event.query.filter(Event.event_id == event_id).delete()
    db.session.commit()


def create_comment(comment, event, user):
    """ Create and return a new comment on an event by the user """

    new_comment = Comment(comment=comment, event_id=event, user_id=user)

    db.session.add(new_comment)
    db.session.commit()

    return new_comment


def get_all_comments_on_an_event(event_id):
    """ Return all comments on an event """

    comments = Comment.query.filter(Comment.event_id == event_id).all()
    list_comments = []
    if comments:
        for comment in comments:
            dict_comments = {}
            handle = get_handle_by_user_id(comment.user_id)
            dict_comments[handle] = comment.comment
            list_comments.append(dict_comments)

    return list_comments


def create_favorite(event, user):
    """ Create and return a new favorite event by the user """

    favorite = Favorite(event_id=event, user_id=user)

    db.session.add(favorite)
    db.session.commit()

    return favorite


def is_favorite(event, user):
    """ Return True if the event has already been favorited by the user """

    if Favorite.query.filter(Favorite.user_id == user, Favorite.event_id == event).first():
        return True
    else:
        return False


def get_favorite_events_by_user(user_id):
    """ Return all favorite events by a user """

    favorites = Favorite.query.filter(Favorite.user_id==user_id).all()
    events = []
    if favorites:
        for favorite in favorites:
            items, event = get_event_by_id(favorite.event_id)
            events.append(event)

    return events

def remove_favorite(event, user):
    """ Remove event from favorite by the user """

    Favorite.query.filter(Favorite.user_id == user, Favorite.event_id == event).delete()
    db.session.commit()


def create_like(event, user):
    """ Create and return a new like for the event """

    like = Like(event_id=event, user_id=user)

    db.session.add(like)
    db.session.commit()

    return like


def is_like(event, user):
    """ Return True if the event is liked """

    if Like.query.filter(Like.user_id == user, Like.event_id == event).first():
        return True
    else:
        return False


def get_likes_of_event(event_id):
    """ Return likes of an event """

    likes = db.session.query(Like).filter(Like.event_id == event_id).count()

    return likes

def get_events_in_order_of_most_liked():
    """ Return list if events in order on most liked """

    events_count = db.session.query(func.count(Like.user_id), Like.event_id).group_by(Like.event_id).order_by(desc(func.count(Like.user_id))).all()
    events = []
    if events_count:
        for event_count in events_count:
            event_id = event_count[1]
            items, event = get_event_by_id(event_id)
            events.append(event)

    return events


def remove_like(event, user):
    """ Remove like from an event """

    Like.query.filter(Like.user_id == user, Like.event_id == event).delete()
    db.session.commit()


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


def get_items_by_keyword(keyword):
    """ Search by keyword and return all events """

    items = Item.query.filter((Item.description.like(f'%{keyword}%')) | (Item.name.like(f'%{keyword}%'))).all()
    
    return items


def get_event_by_item(item):
    """ Return event that has that item """

    event_item = EventsItems.query.filter(EventsItems.item_id==item.item_id).first()
    items, event = get_event_by_id(event_item.event_id)
    print("*"*50)
    print("||||||||| event : ", event)
    print("*"*50)

    return get_event_by_id(event_item.event_id)


def update_item(item_id, name, description, link):
    """ Edit item details and save them """

    item = get_item_by_id(item_id)
    Item.query.filter(Item.item_id == item_id).update(
        {
            "name" : name,
            "description" : description,
            "link" : link
        }
    )

    db.session.commit()

    return item


def edit_item_image(item_id, img_id):
    """ Edit item image and save it """

    item = get_item_by_id(item_id)
    Item.query.filter(Item.item_id == item_id).update(
        {
            "img_id" : img_id
        }
    )
    db.session.commit()

    return item


def delete_item(item_id):
    """ Delete item from the Items table """

    item = get_item_by_id(item_id)
    EventsItems.query.filter(EventsItems.item_id == item_id).delete()
    Item.query.filter(Item.item_id == item_id).delete()
    db.session.commit()


if __name__ == '__main__':
    from server import app

    connect_to_db(app)