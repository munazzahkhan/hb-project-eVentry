""" Models for eVentry app """

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """ A user """

    # creating a users table
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    handle = db.Column(db.String(20))
    email = db.Column(db.String(30))
    password = db.Column(db.String(20))
    img_id = db.Column(db.Integer, db.ForeignKey("images.img_id"), nullable=True)

    image = db.relationship("Image", backref="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} handle={self.handle} email={self.email}>"


class Theme(db.Model):
    """ An event theme """

    # creating a themes table
    __tablename__ = "themes"

    theme_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    color = db.Column(db.String(30))

    def __repr__(self):
        return f"<Theme theme_id={self.theme_id} name={self.name} color={self.color}>"


class Image(db.Model):
    """ An image """

    # creating a images table
    __tablename__ = "images"

    img_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String)

    def __repr__(self):
        return f"<Image img_id={self.img_id} url={self.url}>"


class Category(db.Model):
    """ A category """

    # creating a categories table
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"<Category category_id={self.category_id} name={self.name}>"


class Event(db.Model):
    """ An event """

    # creating an events table
    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    theme_id = db.Column(db.Integer, db.ForeignKey("themes.theme_id"))
    img_id = db.Column(db.Integer, db.ForeignKey("images.img_id"))

    user = db.relationship("User", backref="events")
    category = db.relationship("Category", backref="events")
    theme = db.relationship("Theme", backref="events")
    image = db.relationship("Image", backref="event")

    def __repr__(self):
        return f"<Event event_id={self.event_id} category={self.category}>"


class Favorite(db.Model):
    """ Middle table for Events and Users (Favorites for Users) """

    # creating a favorites table
    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f"<Favorite favorite_id={self.favorite_id} event_id={self.event_id} user_id={self.user_id}>"


class Like(db.Model):
    """ Middle table for Events and Users (Likes for Events) """

    # creating a likes table
    __tablename__ = "likes"

    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f"<Like like_id={self.like_id} event_id={self.event_id} user_id={self.user_id}>"


class Comment(db.Model):
    """ A Comments Table """

    # creating a comments table
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.Text)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f"<Comment comment_id={self.like_id} comment={self.comment}>"


class EventsItems(db.Model):
    """ Association table for Events and Items """

    # creating an events_items table
    __tablename__ = "events_items"

    events_items = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"))

    def __repr__(self):
        return f"<EventsItems events_items={self.events_items} event_id={self.event_id} item_id={self.item_id}>"


class Item(db.Model):
    """ An event item """

    # creating an items table
    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.Text)
    link = db.Column(db.String)
    img_id = db.Column(db.Integer, db.ForeignKey("images.img_id"))

    image = db.relationship("Image", backref="item")

    def __repr__(self):
        return f"<Item item_id={self.item_id} description={self.description}>"


def connect_to_db(flask_app, db_uri="postgresql:///eventry", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
