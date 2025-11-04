import os

TARGET_COLUMN = "class"
PIPELINE_NAME = "sensor"
ARTIFACT_DIR = "artifact"
FILE_NAME = "sensor.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")
SCHEME_DROP_COLUMNS = "drop_columns"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"

"""
data ingestion related constant values(folder names, file names etc.)
"""

DATA_INGESTION_COLLECTION_NAME: str = "sensor"
DATA_INGESTION_DIR_NAME: str = "artifact"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2