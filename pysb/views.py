"""Website views"""

import base64
import json
import os
from html import escape as escape_html
from shutil import rmtree
from typing import Any

from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory)

from .config import MAX_PASTE_COUNT, MAX_PASTE_SIZE_B, PASTE_DIR
from .util import limit_content_length, unique_filename

views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index() -> str:
    """Home page"""

    if not os.path.exists(PASTE_DIR):
        os.makedirs(PASTE_DIR, exist_ok=True)

    return render_template(
        "index.j2", title="paste", paste_count=len(os.listdir(PASTE_DIR))
    )


@views.route("/", methods=["POST"])
@limit_content_length(MAX_PASTE_SIZE_B)
def paste() -> Any:
    """Save a paste to disk"""

    if MAX_PASTE_COUNT is not None and len(os.listdir(PASTE_DIR)) >= MAX_PASTE_COUNT:
        rmtree(PASTE_DIR)
        os.makedirs(PASTE_DIR, exist_ok=True)

    filename = unique_filename(PASTE_DIR)

    with open(os.path.join(PASTE_DIR, filename), "w") as f:
        paste_json = {
            "text": request.form["paste"],
            "author": request.form["author"],
            "name": request.form["name"],
        }

        for key in paste_json.keys():
            paste_json[key] = base64.b64encode(paste_json[key].encode()).decode()

        json.dump(paste_json, f, indent=0)

    return redirect(f"/p/{filename}")


@views.route("/p/<paste_name>", methods=["GET"])
def get_paste(paste_name) -> Any:
    """Get paste from disk"""

    try:
        with open(os.path.join(PASTE_DIR, paste_name), "r") as p:
            paste_json = json.load(p)

            paste_json["paste_id"] = paste_name
            paste_json["title"] = paste_name

            for key in paste_json:
                try:
                    paste_json[key] = escape_html(
                        base64.b64decode(paste_json[key]).decode()
                    )
                except UnicodeError:
                    pass

            return render_template("paste.j2", **paste_json)
    except FileNotFoundError:
        flash(f"Paste /{escape_html(paste_name)}/ not found", "error")
        return redirect("/messages")


@views.route("/messages", methods=["GET"])
def get_server_messages() -> str:
    """Get flashed messages"""

    return render_template("msg.j2", title="messages")


@views.route("/favicon.ico")
def favicon() -> Any:
    """Icon"""

    return send_from_directory(
        os.path.join(views.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
