#!/usr/bin/env python3
"""Module for 0-app"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """Returns the template"""
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run()
