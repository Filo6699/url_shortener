from dotenv import load_dotenv
import os

load_dotenv()

bind = "0.0.0.0:5000"  # Change the port if needed
workers = 1  # Adjust the number of workers based on your requirements
if os.getenv("SSL") == 'on':
    keyfile = os.getenv("SSL_PRIVATE_KEY_PATH")
    certfile = os.getenv("SSL_CERTIFICATE_PATH")
