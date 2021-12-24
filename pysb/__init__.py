"""Main components"""

import logging
import os
from logging.config import dictConfig as logging_dict_config
from typing import Any

from flask import Flask, flash, g, redirect
from flask_limit import RateLimiter

from .config import (LOG_DIR, LOGGING_CONFIG, PASTE_DIR, REQUEST_CODES,
                     SECRET_KEY, WEBSITE_NAME, RequestLimiterConfig)


def create_app() -> Flask:
    """Make a new app"""

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

    logging_dict_config(LOGGING_CONFIG)

    app = Flask(__name__)
    log = logging.getLogger(__name__)

    os.makedirs(PASTE_DIR, exist_ok=True)

    app.config.from_object(RequestLimiterConfig)
    app.config["SECRET_KEY"] = SECRET_KEY

    limiter = RateLimiter(app)

    @app.errorhandler(Exception)
    def http_error_handler(error) -> Any:
        try:
            flash(
                f"{error} ~ HTTP/{error.code}",
                REQUEST_CODES.get(error.code) or "http_errno",
            )
        except AttributeError:
            err_msg = f"{error.__class__.__name__}: {error} ~ http_fatal_errno"
            log.error(err_msg)

            return err_msg, 500

        return redirect("/messages", 308)

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

    del before_request, after_request, context, http_error_handler

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
