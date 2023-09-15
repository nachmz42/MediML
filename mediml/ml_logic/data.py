from pathlib import Path

import pandas as pd
from colorama import Fore, Style
from google.cloud import bigquery

from mediml.params import (DATASET, LOCAL_DATA_PATH, PIPELINE_TARGET, PROJECT,
                           TABLE)


def load_data() -> pd.DataFrame:
    '''
    Load data
    - Locally, from raw_data folder
    - From BigQuery
    '''

    df = pd.DataFrame()

    if PIPELINE_TARGET == "local":
        print(Fore.BLUE + f"\nLoad data from local disk..."
              + Style.RESET_ALL)

        # Load raw data from local repository
        data_exists = LOCAL_DATA_PATH.is_file()

        if not data_exists:
            print(Fore.YELLOW +
                  f"⏳ Downloading data from https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset" + Style.RESET_ALL)
            raise FileNotFoundError

        df = fetch_cached_data()

    elif PIPELINE_TARGET == "gcs":
        query = f"""       
          SELECT *
          FROM {PROJECT}.{DATASET}.{TABLE}
          """

        # Retrieve `query` data from BigQuery or from `data_query_cache_path` if the file already exists!
        data_query_cached_exists = LOCAL_DATA_PATH.is_file()

        if data_query_cached_exists:
            print("Loading data from local CSV...")
            df = fetch_cached_data()

        else:
            print("Loading data from Querying Big Query server...")

            client = bigquery.Client(project=PROJECT)
            query_job = client.query(query)
            result = query_job.result()
            df = result.to_dataframe()

            # Save it locally to accelerate the next queries!
            df.to_csv(LOCAL_DATA_PATH, header=True, index=False)

    if df.empty:
        print(Fore.YELLOW +
              f"⚠️ No data found could be loaded" + Style.RESET_ALL)
        raise FileNotFoundError

    # Make sure the id column is the index of the dataFrame
    df.set_index('id', inplace=True)
    return df


def fetch_cached_data() -> pd.DataFrame:
    '''
    Fetch cached data
    '''
    df = pd.read_csv(LOCAL_DATA_PATH)
    return df
