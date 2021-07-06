# <img src="https://github.com/munazzahkhan/hb-project-eVentry/blob/master/static/images/logo/logo_gold.png" width="20%">
There is no one-stop-shop with information and instructions on how to pull off a successful event, eVentry is here to provide you exactly that. eVentry (where creativity shines) is a web application to share and manage an inventory of event ideas, where members can share their events and talk about how, why and where they got various elements. It uses a PostgresQL database to store user added data and is built with a Python/Flask backend.

## About the Developer
Munazzah graduated with a masters degree in CS. Soon after graduation, she moved to the United States on a non-work visa. Munazzah immersed herself in arts & crafts classes and also became involved in event management, as they brought joy and excitement to her life.  She became eligible to legally work in the US but by this time, her software engineering skills were a bit rusty and she was behind on industry trends. Munazzah has always been passionate about problem solving and algorithms. Recently, her path led her back to computer science and reignited her passion for software engineering. She is excited about finally pursuing her dream and passion in IT and software engineering.

## Deployment
<n/>http://34.218.45.14/

## Contents
* [Tech Stack](#tech-stack)
* [Data Model](#data-model)
* [Features](#features)
* [Future State](#future)
* [Installation](#installation)

## <a name="tech-stack"></a>Tech Stack
* Python
* Flask
* WTForms
* HTML
* Jinja
* Bootstrap
* CSS
* PostgresQL
* SQLAlchemy
* JavaScript
* jQuery

## <a name="data-model"></a>Data Model

![Data Model](static/images/readme/data_model.png)

## <a name="features"></a>Features

#### Homapage
Homepage displays event categories in the left navbar and the most liked events in the right pane. 

![Homepage](static/images/readme/homepage.png)

#### Sign up/Sign in
Members can sign up or sign in.

![Sign up/Sign in](static/images/readme/signup_signin.gif)

#### Profile Page
From the top navbar, signed in members can view their profile page by clicking on "My Profile".

![Profile Page](static/images/readme/profile_page.png)

#### Event Categories
From the side navbar, members can see events of a specific category.

![Event Categories](static/images/readme/event_categories.gif)

#### My Event
From "My Events" tab, members can view their events, edit/delete event details, items, item details and all the images by clicking on the event.

![My Events](static/images/readme/my_events.gif)

#### Create an Event
From "Create New Event" tab, members can add an event followed by event items with all the details. The new event will show up in "My Events" tab for the member.

![Add Event](static/images/readme/add_event.gif)
![Add Items](static/images/readme/add_items.gif)

#### Favorite & Likes
From "Favorites" tab, members can view all the events that they have favorited.

![Favorites](static/images/readme/favorites.png)

When members view any event, they can add it to their favorites by clicking the heart icon and/or like an event by clicking the thumbs up icon.

![Favorite/Like](static/images/readme/Favourite_like.gif)

#### Search
From the search bar on the top right, members can search for a keyword. Results will be displayed as events & event items matching the keyword.

![Search](static/images/readme/search.gif)

#### Sign out
A member's session is invalidated when they click the "Sign out" tab.

![Sign out](static/images/readme/sign_out.gif)

## <a name="future"></a>Future Work
Future features that are in plans for eVentry include:

* Creating event invites and sending them to guests. 
* Option to the members who are good at DIYs 
  - To host a class for their DIYs.
  - To sell their DIYs.
* Incorporating Ads that are relevant to various events, items and members by implementing Ad slots on the web page.

## <a name="installation"></a>Installation Guide

Here is a step by step guidline to run eVentry on a local machine

* Install PostgresQL following this link **https://www.postgresql.org/download/**

* Clone this repo
```
https://github.com/munazzahkhan/hb-project-eVentry
```
* Create and activate a virtual environment inside your eVentry directory
```
virtualenv env
source env/bin/activate
```
* Install the dependencies
```
pip install -r requirements.txt
```
* Set up the database
```
python3 seed.py
```
* Run the app
```
python3 server.py
```
* Follow the following link to access eVentry
**http://localhost:5000**

Once the website is up and running you can either create new account, or use these accounts that were added as part of seed.py:
|email|password|
|--|--|
|email1@gmail.com|password|
|email2@gmail.com|password|
|email3@gmail.com|password|
|email4@gmail.com|password|
