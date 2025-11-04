from sensor.exception import SensorException
import sys
import os
from sensor.logger import logging
from sensor.utils import dump_csv_file_to_monogodb_collection
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainPipeline
# def test_exception():
#     try:
#         logging.info("Testing logging")
#         a = 1/0
#     except Exception as e:
#         raise SensorException(e,sys)

if __name__ ==  "__main__":  # sets the module. Makes sure the variables of imported files are not confused with variables in this file
    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)
    #file_path = "/Users/bhavyamehta/Desktop/SensorLive_Workplace/aps_failure_training_set1.csv"
    #database_name = "APS"
    #collection_name = "sensor"
    #dump_csv_file_to_monogodb_collection(file_path, database_name, collection_name)


    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()