""" Script to seed database """

import os
from random import choice, randint

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()


colors = ['red', 'green', 'blue', 'yellow', 'teal', 'pink', 'peach', 'white', 'gold', 'orange']

for n in range(10):

    fname = f'first{n}'
    lname = f'last{n}'
    email = f'user{n}@test.com'
    password = 'test'

    new_user = crud.create_user(fname, lname, email, password)

    theme = f'theme{n}'
    color = choice(colors)

    new_theme = crud.create_theme(theme, color)

    category = choice(['birthday', 'babyshower'])

    r = randint(1,3)
    url = f'\images\event-{r}'

    image = crud.create_image(url)

    new_event = crud.create_event(new_user, category, theme, image)

    for i in range(5):

        description = f'This is item{i}. I got it from a store.'
        link = f'Here is the link for item{i}'
        r = randint(1,3)
        url = f'\images\item-{r}'

        image = crud.create_image(url)

        new_item = crud.create_item(description, link, image)
