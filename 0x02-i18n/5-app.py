#!/usr/bin/env python3
"""Module for 5-app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

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
    """Retrieve user by ID."""
    user_id = request.args.get('login_as')
    if user_id and int(user_id) in users:
        return users[int(user_id)]
    return None

@app.before_request
def before_request():
    """Execute before each request."""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Determine the best match with our supported languages"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """Renders template"""
    return render_template('5-index.html')

if __name__ == "__main__":
    app.run()
