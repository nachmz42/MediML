import os
from pathlib import Path

##################  VARIABLES  ##################
PIPELINE_TARGET = os.environ.get("PIPELINE_TARGET")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
PROJECT = os.environ.get("PROJECT")
DATASET = os.environ.get("DATASET")
TABLE = os.environ.get("TABLE")


##################  CONSTANTS  #####################
LOCAL_DATA_PATH = Path("raw_data/healthcare-dataset-stroke-data.csv")
LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser(
    '~'), ".mediml", "mlops", "training_outputs")
PIPELINE_DIRECTORY = "pipelines"

COLUMN_NAMES_RAW = ['gender',
                    'age',
                    'hypertension',
                    'heart_disease',
                    'ever_married',
                    'work_type',
                    'Residence_type',
                    'avg_glucose_level',
                    'bmi',
                    'smoking_status']
