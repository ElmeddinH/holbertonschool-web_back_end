#!/usr/bin/env python3
"""Flask app with timezone inference from URL, user settings, or default."""
from typing import Dict, Optional, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
import pytz
from pytz import UnknownTimeZoneError

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for the Flask application."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


def get_user() -> Optional[Dict[str, Optional[str]]]:
    """Retrieve a user dict based on login_as URL parameter.

    Returns the user dict if found, None otherwise.
    """
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request() -> None:
    """Set the current user on flask.g before each request."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Determine locale with priority order.

    Priority:
    1. URL ?locale= parameter
    2. Logged-in user's locale preference
    3. Request Accept-Language header
    4. Default locale
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> Optional[str]:
    """Determine the appropriate timezone with priority order.

    Priority:
    1. URL ?timezone= parameter
    2. Logged-in user's timezone preference
    3. Default timezone (UTC)
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    if g.user:
        user_tz = g.user.get('timezone')
        if user_tz:
            try:
                pytz.timezone(user_tz)
                return user_tz
            except UnknownTimeZoneError:
                pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index() -> str:
    """Render the index page with user login info and current time."""
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run()
