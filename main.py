from dotenv import load_dotenv
from db import DB
import os
from hash import shorten_url
from json import loads
from flask import Flask, jsonify, request, redirect, render_template


app = Flask(__name__)


@app.route("/<string:url>", methods=['GET'])
def url(url):
    redirect_url = DB.find_url(url)
    if redirect_url:
        redirect_url = redirect_url[0]
    else:
        return render_template("not_found.html")
    return redirect(redirect_url)


@app.route("/list_urls", methods=['GET'])
def admin():
    admin_key = request.headers.get("Authorization")
    if admin_key != os.getenv("admin_key"):
        return jsonify({"message": "Unauthorized"}, 401)
    urls = DB.view_urls()
    return jsonify({"url_list": urls})


@app.route("/tables", methods=['GET'])
def tables():
    names = DB.fetch_table_names()
    return jsonify({"tables": names})


@app.route("/upload", methods=['POST'])
def upload_url():
    data: dict = loads(request.data)
    full_url = data.get('url')
    if not full_url:
        return jsonify({"message": "No url provided"}, 400)
    short_url = shorten_url(full_url)
    if not DB.find_url(short_url):
        DB.insert_url(short_url, full_url)
    return jsonify({"message": "Uploaded", "data": short_url}, 200)


@app.route("/", methods=['GET'])
def main():
    return render_template("index.html")


if __name__ == "__main__":
    load_dotenv(),
    DB.connect()
    app.run("0.0.0.0", port=5000)
