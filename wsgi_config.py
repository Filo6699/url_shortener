from dotenv import load_dotenv

load_dotenv()

bind = "0.0.0.0:5000"  # Change the port if needed
workers = 3  # Adjust the number of workers based on your requirements
keyfile = os.getenv("SSL_PRIVATE_KEY_PATH")
certfile = os.getenv("SSL_CERTIFICATE_PATH")
