import os

##################  VARIABLES  ##################
PIPELINE_TARGET = os.environ.get("PIPELINE_TARGET")
BUCKET_NAME = os.environ.get("BUCKET_NAME")


##################  CONSTANTS  #####################
LOCAL_DATA_PATH = os.path.join(
    os.path.expanduser('~'), ".mediml", "mlops", "data")
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
