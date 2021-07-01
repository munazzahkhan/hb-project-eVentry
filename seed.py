""" Script to seed database """

import os
import json
from random import choice, randint

import crud
import model
import server

os.system('dropdb eventry')
os.system('createdb eventry')

model.connect_to_db(server.app)
model.db.create_all()

CATEGORIES = ['Anniversary', 'Baby Shower', 'Birthday', 'Bridal Shower', 'Graduation', 'Halloween', 'Pool Party', 'Wedding Reception', '4th of July']
COMMENTS = [
            'Love this idea',
            'Wow! I am going to use this theme',
            'So cute',
            'What a thoughtful event',
            'Totally what I would do <3!',
            'How incredible is this ... WoW!',
            'I so wanted to try this. Thank you for sharing!',
            'This is helpful. Yay!',
            'Love love love',
            'Creativity at its peak!',
            'I like this so much',
            'Gonna start working on this ASAP',
            'So dope!',
            'Wish I seen this earlier. So amazing.',
            'Just amazing!',
            'oh man! That is what I call an event',
            'After looking at this, I just want to host :)',
            'What an event!',
            'This looks wonderful!',
            'So neat!'
            ]

for category in CATEGORIES:
    crud.create_category(category)


with open('data/users.json') as u:
    user_data = json.loads(u.read())

users_in_db = []
for user in user_data:
    fname = user["fname"]
    lname = user["lname"]
    handle = user["handle"]
    email = user["email"]
    password = user["password"]
    user_image = user["image"]

    image = crud.create_image(user_image)
    new_user = crud.create_user(fname, lname, handle, email, password, image.img_id)
    users_in_db.append(new_user)


with open('data/events.json') as e:
    event_data = json.loads(e.read())

events_in_db = []
for event in event_data:
    color = event["color"]
    category = event["category"]
    event_image = event["event_image"]
    description = event["event_description"]
    items_data = event["items"]

    new_theme = crud.create_theme(color)
    image = crud.create_image(event_image)

    user = choice(users_in_db)
    new_event = crud.create_event(description, user.user_id, category, new_theme.theme_id, image.img_id)

    for item in items_data:
        name = item["name"]
        description = item["item_description"]
        link = item["link"]
        item_image = item["item_image"]

        image = crud.create_image(item_image)
        new_item = crud.create_item(name, description, link, image.img_id)
        crud.create_events_items(new_event.event_id, new_item.item_id)
    
    events_in_db.append(new_event)

for i in range(80):

    user = choice(users_in_db)
    event = choice(events_in_db)

    if not crud.is_favorite(event.event_id, user.user_id):
        crud.create_favorite(event.event_id, user.user_id)

    user = choice(users_in_db)
    event = choice(events_in_db)

    if not crud.is_like(event.event_id, user.user_id):
        crud.create_like(event.event_id, user.user_id)
    
    user = choice(users_in_db)
    event = choice(events_in_db)
    comment = choice(COMMENTS)

    if not crud.is_event_by_user(user.user_id, event.event_id):
        crud.create_comment(comment, event.event_id, user.user_id)