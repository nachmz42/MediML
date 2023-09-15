import glob
import os
import pickle
import time

from colorama import Fore, Style
from google.cloud import storage
from imblearn.pipeline import Pipeline

from mediml.params import (BUCKET_NAME, LOCAL_REGISTRY_PATH,
                           PIPELINE_DIRECTORY, PIPELINE_TARGET)


def load_pipeline() -> Pipeline | None:
    """
    Return a saved pipeline:
    - locally (latest one in alphabetical order), raise FileNotFoundError if no pipeline is found
    - on GCS (latest one by timestamp), raise Exception if no pipeline is found
    """

    if PIPELINE_TARGET == "local":
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

    if PIPELINE_TARGET == "gcs":
        print(Fore.BLUE + f"\nLoad latest pipeline from GCS..." + Style.RESET_ALL)

        client = storage.Client()
        blobs = list(client.get_bucket(
            BUCKET_NAME).list_blobs(prefix=PIPELINE_DIRECTORY))

        try:
            latest_blob = max(blobs, key=lambda x: x.updated)
            latest_pipeline_path_to_save = os.path.join(
                LOCAL_REGISTRY_PATH, latest_blob.name)
            latest_blob.download_to_filename(latest_pipeline_path_to_save)

            latest_pipeline = pickle.load(
                open(latest_pipeline_path_to_save, "rb"))

            print(f"✅ Latest pipeline found at {latest_pipeline_path_to_save}")

            print("✅ Latest pipeline downloaded from cloud storage")

            return latest_pipeline
        except:
            print(f"\n❌ No pipeline found in GCS bucket {BUCKET_NAME}")
            raise Exception("No pipeline found in GCS bucket")

    print(Fore.YELLOW + f"\n No model target specified" + Style.RESET_ALL)

    return None


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

    if PIPELINE_TARGET == "gcs":
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
