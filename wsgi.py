from main import app, init, shutdown
import atexit

atexit.register(shutdown)
init()
