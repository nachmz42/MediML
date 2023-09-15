import glob
import os
import pickle
import time

from colorama import Fore, Style
from google.cloud import storage
from imblearn.pipeline import Pipeline

from mediml.params import (BUCKET_NAME, LOCAL_REGISTRY_PATH, MODEL_TARGET,
                           PIPELINE_DIRECTORY)


def load_pipeline() -> Pipeline:
    """
    Return a saved pipeline:
    - locally (latest one in alphabetical order)

    Raise FileNotFoundError if no pipeline is found
    """

    print(Fore.BLUE + f"\nLoad latest pipeline from local registry..."
          + Style.RESET_ALL)

    # Get the latest pipeline version name by the timestamp on disk
    local_pipeline_directory = os.path.join(
        LOCAL_REGISTRY_PATH, PIPELINE_DIRECTORY)
    local_pipeline_paths = glob.glob(f"{local_pipeline_directory}/*")

    if not local_pipeline_paths:
        print(Fore.YELLOW +
              f"⚠️ No pipeline found in {local_pipeline_directory}"
              + Style.RESET_ALL)
        raise FileNotFoundError

    most_recent_pipeline_path_on_disk = sorted(local_pipeline_paths)[-1]

    print(f"✅ Pipeline found at {most_recent_pipeline_path_on_disk}")

    print(Fore.BLUE + f"\nLoad latest pipeline from disk..." + Style.RESET_ALL)

    latest_pipeline = pickle.load(
        open(most_recent_pipeline_path_on_disk, "rb"))

    print("✅ Pipeline loaded from local disk")

    return latest_pipeline


def save_pipeline(pipeline: Pipeline) -> None:
    """
    Persist trained pipeline
    - Locally at "{LOCAL_REGISTRY_PATH}/pipelines/{current_timestamp}.pkl"
    - on GCS at "{BUCKET_NAME}/pipelines/{current_timestamp}.pkl"
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")  # e.g. 20210824-154952

    # Save pipeline locally
    pipeline_path = os.path.join(
        LOCAL_REGISTRY_PATH, PIPELINE_DIRECTORY, f"{timestamp}.pkl")
    pickle.dump(pipeline, open(pipeline_path, 'wb'))

    print("✅ Pipeline saved locally")

    if MODEL_TARGET == "gcs":
        # e.g. "20230208-161047.pkl" for instance
        pipeline_filename = pipeline_path.split("/")[-1]
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"{PIPELINE_DIRECTORY}/{pipeline_filename}")
        blob.upload_from_filename(pipeline_path)

        print("✅ Pipeline saved to GCS")

        return None

    return None


def save_results(metrics: dict) -> None:
    """
    Persist metrics locally on the hard drive at
    "{LOCAL_REGISTRY_PATH}/metrics/{current_timestamp}.pickle"
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Save metrics locally
    if metrics is not None:
        metrics_path = os.path.join(
            LOCAL_REGISTRY_PATH, "metrics", timestamp + ".pickle")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    print("✅ Results saved locally")
