import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_HOSTS = [os.environ.get("HOST_ADDRESS")]

INTERNAL_IPS = [os.environ.get("HOST_ADDRESS")]
