from pathlib import Path

import pandas as pd
from google.cloud import bigquery

from mediml.environment.params import DATASET, LOCAL_DATA_PATH, PROJECT, TABLE


def load_data() -> pd.DataFrame:
    '''
    Load data
    - Locally, if the file exists
    - From BigQuery otherwise
    '''

    query = f"""
    SELECT *
    FROM {PROJECT}.{DATASET}.{TABLE}
    """

    # Retrieve `query` data from BigQuery or from `data_query_cache_path` if the file already exists!
    data_query_cached_exists = Path(LOCAL_DATA_PATH).is_file()
    
    if data_query_cached_exists:
        print("Loading data from local CSV...")

    else:
        print("Loading data from Querying Big Query server...")

        client = bigquery.Client(project=PROJECT)
        query_job = client.query(query)
        result = query_job.result()
        df_from_big_query = result.to_dataframe()

        # Save it locally to accelerate the next queries!
        df_from_big_query.to_csv(LOCAL_DATA_PATH, header=True, index=False)

    df = pd.read_csv(LOCAL_DATA_PATH)

    # Make sure the id column is the index of the dataFrame
    df.set_index('id', inplace=True)
    return df
