import os
import sys
import logging
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from distutils import dir_util     # to use the files in util folder
from sensor.exception import SensorException
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
import pandas as pd
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp # to check drifting
class DataValidation:
    def __init__(self, data_validation_config : DataValidationConfig, data_ingestion_artifact : DataIngestionArtifact):
        try: 
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            
        except Exception as e:
            raise SensorException(e, sys)
        
    @staticmethod # no need to create an object to use this function anywhere else
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)
        
    def validate_number_of_columns(self, dataframe : pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                logging.info("Column names in dataframe match schema.")
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)
        
    def validate_numeric_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            numeric_columns = self._schema_config["numerical_columns"]
            df_columns = dataframe.columns

            missing_numeric_columns = []
            for cols in numeric_columns:
                if cols not in df_columns:
                    missing_numeric_columns.append(cols)

            logging.info(f"Missing numeric columns: {missing_numeric_columns}")
            if len(missing_numeric_columns) > 0:
                return False
            return True
        
        except Exception as e:
            raise SensorException(e, sys)
        
    def detect_dataset_drift(self, d1, d2, threshold = 0.05) -> bool:
        try:
            status = True
            report ={}
            for cols in d1.columns:
                db1 = d1[cols]
                db2 = d2[cols]   
                is_same_dist = ks_2samp(db1, db2)
                if threshold <= is_same_dist.pvalue:
                    drift = False
                else:
                    drift = True
                    status = False
                report.update({cols:{
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": drift
                }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            write_yaml_file(drift_report_file_path, report,)
            return status
        
        except Exception as e:
            raise SensorException(e, sys)
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # READING DATA FROM TRAIN AND TEST FILE LOCATION
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # VALIDATING NUMBER OF COLUMNS
            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain all columns.\n"

            # VALIDATING NUMERIC COLUMNS
            status = self.validate_numeric_columns(dataframe=train_df)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all numeric columns.\n"
            status = self.validate_numeric_columns(dataframe=test_df)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain all numeric columns.\n"

            # VALIDATING DATA DRIFT
            status = self.detect_dataset_drift(d1=train_df, d2=test_df)
            if not status:
                error_message = f"{error_message}Train and test dataset has different distribution.\n"

            if len(error_message)>0:
                raise Exception(error_message)

            data_validation_artifact = DataValidationArtifact(
                validation_status= status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path= None,
                invalid_test_file_path= None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path)
            
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise SensorException(e, sys)
