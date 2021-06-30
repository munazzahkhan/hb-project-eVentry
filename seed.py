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


# colors = ['red', 'green', 'blue', 'yellow', 'teal', 'pink', 'peach', 'white', 'gold', 'orange']
CATEGORIES = ['Anniversary', 'Baby Shower', 'Birthday', 'Bridal Shower', 'Graduation', 'Halloween', 'Pool Party', 'Wedding Reception', '4th of July']


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





# for n in range(10):

    # fname = f'first{n}'
    # lname = f'last{n}'
    # handle = f'fl{n}'
    # email = f'user{n}@test.com'
    # password = 'test'
    # k = randint(1,3)
    # p_url = f'/static/images/profiles/profile-{k}.png'
    # image = crud.create_image(p_url)
    # new_user = crud.create_user(fname, lname, handle, email, password, image.img_id)

    # color = choice(colors)

    # new_theme = crud.create_theme(color)

    # category = randint(1,9)

    # r = randint(1,3)
    # url = f'/static/images/events/event-{r}.jpeg'
    # image = crud.create_image(url)
    # description = f'This is event{n}. I organised it all by myself. Following are some of the items I used to make this a success.'

    # new_event = crud.create_event(description, new_user.user_id, category, new_theme.theme_id, image.img_id)

    # for i in range(5):
    #     name = f'item{i}'
    #     description = f'This is item{i}. I got it from a store.'
    #     link = f'Here is the link for item{i}'
    #     r = randint(1,3)
    #     url = f'/static/images/items/item-{r}.jpeg'

    #     image = crud.create_image(url)

    #     new_item = crud.create_item(name, description, link, image.img_id)

    #     crud.create_events_items(new_event.event_id, new_item.item_id)
