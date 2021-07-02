# <img src="https://github.com/munazzahkhan/hb-project-eVentry/blob/master/static/images/logo/logo_gold.png" width="20%">
Since there is no one-stop-shop with information and instructions on how to pull off a successful event, eVentry is here to provide you exactly that. eVentry (where creativity shines) is a web application to share and manage an inventory of event ideas, where members can share their events and talk about how, why and where they got various elements. It uses a PostgresQL database to store user added data and is built with a Python/Flask backend.

## Contents
* [Tech Stack](#tech-stack)
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

## <a name="features"></a>Features

## <a name="future"></a>Future Plans
Future features that are in plans for eVentry include:

* Creating event invites and sending them to guests. 
* Option to the members who are good at DIYs 
  - To host a class for their DIYs.
  - To sell their DIYs.
* Incorporating Ads that are relevant to various events, items and members by implementing Ad slots on the web page.

## <a name="installation"></a>Installation Guide

Here are step by step guidlines to run eVentry on your own machine:

* Install PostgresQL
* Clone this repo:
```
https://github.com/munazzahkhan/hb-project-eVentry
```
* Create and activate a virtual environment inside your eVentry directory:
```
virtualenv env
source env/bin/activate
```
* Install the dependencies:
```
pip install -r requirements.txt
```
* Set up the database:
```
python3 seed.py
```
* Run the app:
```
python3 server.py
```
* Follow the following link to access eVentry:
**http://localhost:5000**

Once the website is up and running you can either create new account, or use these accounts that were added as part of seed.py:
|email|password|
|--|--|
|email1@outlook.com|password|
|email2@outlook.com|password|
|email3@outlook.com|password|
