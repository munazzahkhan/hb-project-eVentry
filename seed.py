""" Script to seed database """

import os
from random import choice, randint

import crud
import model
import server

os.system('dropdb eventry')
os.system('createdb eventry')

model.connect_to_db(server.app)
model.db.create_all()


colors = ['red', 'green', 'blue', 'yellow', 'teal', 'pink', 'peach', 'white', 'gold', 'orange']
categories = ['Birthday', 'Baby Shower']

for category in categories:
    crud.create_category(category)

print(model.Category.query.all())

for n in range(10):

    fname = f'first{n}'
    lname = f'last{n}'
    email = f'user{n}@test.com'
    password = 'test'

    new_user = crud.create_user(fname, lname, email, password)

    theme = f'theme{n}'
    color = choice(colors)

    new_theme = crud.create_theme(theme, color)

    category = choice([1,2])

    r = randint(1,3)
    url = f'/static/images/event-{r}.jpeg'

    image = crud.create_image(url)

    new_event = crud.create_event(new_user.user_id, category, new_theme.theme_id, image.img_id)

    for i in range(5):

        description = f'This is item{i}. I got it from a store.'
        link = f'Here is the link for item{i}'
        r = randint(1,3)
        url = f'/static/images/item-{r}.jpeg'

        image = crud.create_image(url)

        new_item = crud.create_item(description, link, image.img_id)

        crud.create_events_items(new_event.event_id, new_item.item_id)
