#!/usr/bin/env python3
"""Module for 3-app"""
from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """Sets the default language and timezone"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale() -> Union[str, None]:
    """Determine the best match with our supported languages"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Returns the templates"""
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run()
