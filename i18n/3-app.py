#!/usr/bin/env python3
"""Flask app with parametrized templates using Flask-Babel translations."""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration class for the Flask application."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)


def get_locale() -> str:
    """Determine best locale from request Accept-Language header."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel = Babel(app, locale_selector=get_locale)


@app.route('/')
def index() -> str:
    """Render the index page with translated content."""
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run()
