#!/usr/bin/env python3
"""Flask app that allows forcing locale via URL parameter."""
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
    """Determine locale from URL parameter, then Accept-Language header.

    Priority: URL ?locale= parameter > request Accept-Language header.
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel = Babel(app, locale_selector=get_locale)


@app.route('/')
def index() -> str:
    """Render the index page with translated content."""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run()
