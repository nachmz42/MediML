from pathlib import Path

import pandas as pd
from colorama import Fore, Style

from mediml.params import LOCAL_DATA_PATH


def load_data() -> pd.DataFrame:
    '''
    Load data
    - Locally, from raw_data folder
    '''

    print(Fore.BLUE + f"\nLoad data from local disk..."
          + Style.RESET_ALL)

    # Load raw data from local repository
    data_exists = LOCAL_DATA_PATH.is_file()

    if not data_exists:
        print(Fore.YELLOW +
              f"⏳ Downloading data from https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset" + Style.RESET_ALL)
        return None

    df = pd.read_csv(LOCAL_DATA_PATH)

    # Make sure the id column is the index of the dataFrame
    df.set_index('id', inplace=True)

    return df
