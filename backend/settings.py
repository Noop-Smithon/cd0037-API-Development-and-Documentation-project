from dotenv import load_dotenv
import os
load_dotenv()
database_name = os.environ.get("database_name")
user_name = os.environ.get("user_name")
# DB_PASSWORD = os.environ.get("DB_PASSWORD")