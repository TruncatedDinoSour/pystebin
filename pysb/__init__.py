"""Main components"""

import os
from typing import Any

from flask import Flask, flash, g, redirect
from flask_limit import RateLimiter

from .config import PASTE_DIR, SECRET_KEY, WEBSITE_NAME, RequestLimiterConfig


def create_app() -> Flask:
    """Make a new app"""

    app = Flask(__name__)
    try:
        os.mkdir(PASTE_DIR)
    except FileExistsError:
        pass

    app.config.from_object(RequestLimiterConfig)
    app.config["SECRET_KEY"] = SECRET_KEY

    limiter = RateLimiter(app)

    @app.errorhandler(404)
    def not_found(e: Any) -> Any:
        flash(str(e), "not_found")
        return redirect("/messages")

    @app.context_processor
    def context() -> dict[str, str]:
        return {"website_name": WEBSITE_NAME}

    @app.before_request
    @limiter.rate_limit
    def before_request() -> None:
        pass

    @app.after_request
    def after_request(rv):
        headers = getattr(g, "headers", {})
        rv.headers.extend(headers)
        return rv

    del before_request, after_request, context, not_found

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
