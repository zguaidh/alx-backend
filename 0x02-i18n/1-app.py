#!/usr/bin/env python3
"""Module for 1-app"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Sets the default language and timezone"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@app.route('/')
def index():
    """Returns template"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()
