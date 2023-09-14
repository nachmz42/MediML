from pathlib import Path

import numpy as np
import pandas as pd
from colorama import Fore, Style
from sklearn.model_selection import train_test_split

from mediml.ml_logic.pipeline import build_pipeline
from mediml.ml_logic.registry import load_pipeline, save_pipeline, save_results
from mediml.params import COLUMN_NAMES_RAW


def preprocess_and_train() -> None:
    """
    - Load raw data from local repository
    - Clean and preprocess data
    - Train a Random Forest Classifier
    - Save the pipeline locally
    """

    # Load raw data from local repository
    data_path = Path("raw_data/healthcare-dataset-stroke-data.csv")
    data_exists = data_path.is_file()

    if not data_exists:
        print(Fore.YELLOW +
              f"⏳ Downloading data from https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset" + Style.RESET_ALL)
        return None

    df = pd.read_csv(data_path)

    # Make sure the id column is the index of the dataframe
    df.set_index('id', inplace=True)

    # # Create X and y
    X = df.drop("stroke", axis=1)
    y = df.stroke

    # Split into train & test set
    X_train, X_test, y_train, y_test = train_test_split(X,  # independent variables
                                                        y,  # dependent variable
                                                        test_size=0.2)  # percentage of data to use for test set

    # Build pipeline
    pipeline = build_pipeline()

    # Fit pipeline
    pipeline.fit(X_train, y_train)

    # Score model - accuracy
    acurracy = pipeline.score(X_test, y_test)
    print(f"✅ Model acurracy: {acurracy}")

    # Save pipeline
    save_pipeline(pipeline=pipeline)

    # Save metrics
    save_results(metrics={"accuracy": acurracy})


def pred(X_pred: pd.DataFrame) -> np.ndarray:
    '''
    - Load latest pipeline from local registry
    - Make predictions on new data
    Return predictions as a numpy array
    '''
    print(Fore.MAGENTA + "\n ⭐️ Use case: pred" + Style.RESET_ALL)

    pipeline = load_pipeline()
    y_pred = pipeline.predict(X_pred)

    res = list(map(lambda x: "Stroke" if x == 1 else "No Stroke", y_pred))
    print(f"{res}")

    print(f"✅ pred() done")

    return res


if __name__ == '__main__':
    try:
        # preprocess_and_train()
        pred(pd.DataFrame([['Male', 80.0, 0, 0, 'Yes', 'Govt_job', 'Urban', 148.72, 28.7,
                           'never smoked']], columns=COLUMN_NAMES_RAW))
    except:
        import sys
        import traceback

        import ipdb
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
