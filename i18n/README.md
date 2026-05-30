# i18n - Flask Internationalization

## Description

This project demonstrates how to implement internationalization (i18n) in a Flask web application using Flask-Babel. It covers locale detection, template parametrization, user-based locale/timezone preferences, and timestamp localization.

## Requirements

- Python 3.9
- Ubuntu 20.04 LTS
- pycodestyle 2.5

## Installation

```bash
pip3 install flask flask-babel pytz
```

## Project Structure

```
i18n/
├── 0-app.py              # Task 0: Basic Flask app
├── 1-app.py              # Task 1: Basic Babel setup
├── 2-app.py              # Task 2: Get locale from request
├── 3-app.py              # Task 3: Parametrize templates
├── 4-app.py              # Task 4: Force locale with URL parameter
├── 5-app.py              # Task 5: Mock logging in
├── 6-app.py              # Task 6: Use user locale
├── 7-app.py              # Task 7: Infer appropriate time zone
├── babel.cfg             # Babel extraction configuration
├── translations/
│   ├── en/LC_MESSAGES/
│   │   ├── messages.po   # English translations
│   │   └── messages.mo   # Compiled English translations
│   └── fr/LC_MESSAGES/
│       ├── messages.po   # French translations
│       └── messages.mo   # Compiled French translations
└── templates/
    ├── 0-index.html
    ├── 1-index.html
    ├── 2-index.html
    ├── 3-index.html
    ├── 4-index.html
    ├── 5-index.html
    ├── 6-index.html
    └── 7-index.html
```

## Compile Translations

After editing `.po` files, compile them:

```bash
pybabel compile -d translations
```

To extract and initialize translations from scratch:

```bash
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l en
pybabel init -i messages.pot -d translations -l fr
```

## Tasks

### Task 0 - Basic Flask app
Simple Flask app with a single `/` route outputting "Welcome to Holberton" as title and "Hello world" as h1.

### Task 1 - Basic Babel setup
Added `Config` class with `LANGUAGES = ["en", "fr"]`, `BABEL_DEFAULT_LOCALE = "en"`, `BABEL_DEFAULT_TIMEZONE = "UTC"`. Instantiated `Babel` object.

### Task 2 - Get locale from request
Added `@babel.localeselector` decorated `get_locale()` that uses `request.accept_languages.best_match()`.

### Task 3 - Parametrize templates
Used `_()` / `gettext` in templates. Created `babel.cfg` and translation `.po` files for `en` and `fr`.

### Task 4 - Force locale with URL parameter
`get_locale()` checks for `?locale=` URL parameter first before falling back to Accept-Language header.

### Task 5 - Mock logging in
Added mock `users` dict, `get_user()` function, and `@app.before_request` to set `g.user`.

### Task 6 - Use user locale
`get_locale()` priority: URL param → user setting → Accept-Language → default.

### Task 7 - Infer appropriate time zone
Added `@babel.timezoneselector` decorated `get_timezone()` with pytz validation. Priority: URL param → user setting → default (UTC).

## Running

```bash
python3 0-app.py
```

Test locale forcing:
```
http://localhost:5000/?locale=fr
http://localhost:5000/?locale=en
```

Test user login (Task 5+):
```
http://localhost:5000/?login_as=1   # Balou (fr locale)
http://localhost:5000/?login_as=2   # Beyonce (en locale)
```

Test timezone (Task 7):
```
http://localhost:5000/?timezone=US/Pacific
http://localhost:5000/?login_as=1&locale=fr
```
