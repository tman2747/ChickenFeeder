import os
from dotenv import load_dotenv

load_dotenv()

dns = os.getenv("dns")
usernamemqtt = os.getenv("usernamemqtt")
password = os.getenv("password")

