from dataclasses import dataclass

@dataclass #used for storing data

class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str