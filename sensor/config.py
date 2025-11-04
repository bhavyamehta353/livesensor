from dataclasses import dataclass
import os
import pymongo

@dataclass #decorator for storing data

class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")


env_var = EnvironmentVariable()
MONGO_CLIENT = pymongo.MongoClient(env_var.mongo_db_url)
