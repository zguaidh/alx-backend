#!/usr/bin/env python3
"""Module for 7-app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Union
from pytz import timezone
import pytz.exceptions

app = Flask(__name__)


class Config:
    """Sets the default language and timezone"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Returns user dict if ID can be found"""
    try:
        return users.get(int(request.args.get('login_as')))
    except Exception:
        return None


@babel.localeselector
def get_locale() -> Union[str, None]:
    """Determines best match for supported languages"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Gets the timezone"""
    user = get_user()
    if user:
        locale = user['timezone']
    if request.args.get('timezone'):
        locale = request.args.get('timezone')

    try:
        return timezone(locale).zone
    except Exception:
        return None


@app.before_request
def before_request():
    """Finds user and sets as global on flask.g.user"""
    g.user = get_user()


@app.route('/')
def index() -> str:
    """Renders template"""
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run()
