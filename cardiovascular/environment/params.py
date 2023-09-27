import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")

ENVIRONMENT = os.getenv("ENVIRONMENT") or "development"

# Load variables according to environment (development, production)
load_dotenv(dotenv_path=f".env.{ENVIRONMENT}")


##################  VARIABLES  ##################
PIPELINE_TARGET = os.getenv("PIPELINE_TARGET")
BUCKET_NAME = os.getenv("BUCKET_NAME")
PROJECT = os.getenv("PROJECT")
DATASET = os.getenv("DATASET")
TABLE = os.getenv("TABLE")
LOCAL_MLOPS_DIRECTORY = os.getenv("LOCAL_MLOPS_DIRECTORY") or ".mlops"


##################  CONSTANTS  #####################
LOCAL_DATA_PATH = os.path.join(
    LOCAL_MLOPS_DIRECTORY, "data", "raw", "CVD_cleaned.csv")
LOCAL_TRAINING_OUTPUTS_PATH = os.path.join(
    LOCAL_MLOPS_DIRECTORY, "training_outputs")
PIPELINE_DIRECTORY = "pipelines"

COLUMN_NAMES_RAW = ['General_Health',
                   'Checkup',
                   'Exercise',
                   'Skin_Cancer',
                   'Other_Cancer',
                   'Depression',
                   'Diabetes',
                   'Arthritis',
                   'Sex',
                   'Age_Category',
                   'Height_(cm)',
                   'Weight_(kg)',
                   'BMI',
                   'Smoking_History',
                   'Alcohol_Consumption',
                   'Fruit_Consumption',
                   'Green_Vegetables_Consumption',
                   'FriedPotato_Consumption']
