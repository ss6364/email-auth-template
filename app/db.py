from motor import motor_asyncio
import os
from dotenv import load_dotenv

# mongo db related operations

load_dotenv()  # load .env file

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME] # type: ignore
