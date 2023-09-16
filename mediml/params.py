import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

##################  VARIABLES  ##################
PIPELINE_TARGET = os.getenv("PIPELINE_TARGET")
BUCKET_NAME = os.getenv("BUCKET_NAME")
PROJECT = os.getenv("PROJECT")
DATASET = os.getenv("DATASET")
TABLE = os.getenv("TABLE")


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
