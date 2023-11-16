from decouple import config as env

bind = "0.0.0.0:5000"  # Change the port if needed
workers = 1  # Adjust the number of workers based on your requirements
if env("SSL") == 'on':
    keyfile = env("SSL_PRIVATE_KEY_PATH")
    certfile = env("SSL_CERTIFICATE_PATH")
