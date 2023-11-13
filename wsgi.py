from flask import request, redirect
from main import app, init, shutdown
import atexit

class RedirectMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request_path = environ.get("PATH_INFO", "")
        if "wp-includes" in request_path:
            # Redirect the request to a different URL
            return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ", code=302)(environ, start_response)

        return self.app(environ, start_response)

app.wsgi_app = RedirectMiddleware(app.wsgi_app)

atexit.register(shutdown)
init()
