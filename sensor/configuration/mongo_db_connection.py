from dotenv import load_dotenv
import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
ca = certifi.where()
from sensor.constant.env_variables import MONGODB_URL_KEY
import os
import logging

load_dotenv() # to use os.getenv later on ahead

class MongoDBClient:
    client = None

    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                logging.info(f"Retrieved url for mongo db: {mongo_db_url}")
                
                if "localhost" in mongo_db_url:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
                else:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca) #TLS/SSL
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
        
        except Exception as e:
            logging.error(f"Error initiliazing MongoDB: {e}")
            raise 
    