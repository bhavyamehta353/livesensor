import pandas as pd
import numpy as np
import logging
import json
from sensor.config import MONGO_CLIENT
def dump_csv_file_to_monogodb_collection(file_path:str, database_name:str, collection_name:str)->None: # return nothing
    try:
        df = pd.read_csv(file_path)
        df.reset_index(drop = True, inplace = True)
        json_records = list(json.loads(df.T.to_json()).values())

        MONGO_CLIENT[database_name][collection_name].insert_many(json_records)
        
        logging.info(f"Data imported from {file_path} to MongoDB")
    
    except Exception as e:
        print(e)