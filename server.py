"""Server for eVentry app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud


app = Flask(__name__)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)