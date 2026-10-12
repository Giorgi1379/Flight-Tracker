import os
from dotenv import load_dotenv

load_dotenv()

class config:
    def __init__(self):
        #postgre settings
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "postgres")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "")
        #opensky api settings
        self.api_username = os.getenv("API_USERNAME", "")
        self.api_password = os.getenv("API_PASSWORD", "")

settings = config()