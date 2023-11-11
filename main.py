import json
import logging
import os
import signal
import sys
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, render_template, make_response
from svgwrite import Drawing, text
import validators
from db import DB
from hash import shorten_url

# App creation

def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s %(message)s')

    log_directory = 'logs/'
    os.makedirs(log_directory, exist_ok=True)

    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)

    return app

app = create_app()

@app.before_request
def log_request_info() -> None:
    log = "\nRequest URL: %s\n%s\nData: %s\n"
    data_to_log = str(request.data) if request.data else "No data"
    
    app.logger.debug(log, request.url, str(request.headers).strip(), data_to_log)

# Routes

@app.route("/<string:url>", methods=['GET'])
def redirect_url(url):
    """Redirect to the original URL."""
    redirect_url = DB.find_url(url)
    if redirect_url:
        redirect_url = redirect_url[0]
    else:
        return render_template("not_found.html")
    return redirect(redirect_url)

@app.route("/list_urls", methods=['GET'])
def admin():
    """View the list of URLs (admin access required)."""
    admin_key = request.headers.get("Authorization")
    if admin_key != os.getenv("admin_key"):
        return jsonify({"message": "Unauthorized"}, 401)
    urls = DB.view_urls()
    return jsonify({"url_list": urls})

@app.route("/tables", methods=['GET'])
def tables():
    """View the names of database tables."""
    names = DB.fetch_table_names()
    return jsonify({"tables": names})

@app.route("/upload", methods=['POST'])
def upload_url():
    """Upload a new URL."""
    try:
        data: dict = json.loads(request.data)
    except json.JSONDecodeError as e:
        return make_response(jsonify({"message": f"Invalid data provided: {e}"}), 400)

    full_url = data.get('url')
    if not full_url:
        return make_response(jsonify({"message": "No URL provided"}), 400)
    if not validators.url(full_url) == True:
        return make_response(jsonify({"message": "Not a valid URL"}), 400)
    short_url = shorten_url(full_url)
    if not DB.find_url(short_url):
        DB.insert_url(short_url, full_url)
    return jsonify({"message": "Uploaded", "data": short_url}, 200)

@app.route("/", methods=['GET'])
def main():
    """Render the main page."""
    return render_template("index.html", visits=DB.visits())

# Shutdown Hook

def shutdown(*_):
    """Save visits data on shutdown."""
    DB.save_visits()
    sys.exit(0)

# Application Initialization

if __name__ == "__main__":
    load_dotenv()
    DB.connect()
    signal.signal(signal.SIGINT, shutdown)
    
    # Configure SSL if enabled
    if os.getenv("SSL") == 'on':
        app.run("0.0.0.0", ssl_context=(os.getenv("SSL_CERTIFICATE_PATH"), os.getenv("SSL_PRIVATE_KEY_PATH")))
    else:
        app.run("0.0.0.0")
