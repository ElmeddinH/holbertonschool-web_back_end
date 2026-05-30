#!/usr/bin/env python3
"""Basic Flask application with a single route."""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index() -> str:
    """Render the index page with welcome message."""
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run()
