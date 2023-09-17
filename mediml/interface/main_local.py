from pathlib import Path

import numpy as np
import pandas as pd
from colorama import Fore, Style
from sklearn.model_selection import train_test_split

from mediml.environment.params import COLUMN_NAMES_RAW
from mediml.ml_logic.data import load_data
from mediml.ml_logic.pipeline import build_pipeline
from mediml.ml_logic.registry import load_pipeline, save_pipeline, save_results


def preprocess_train_and_evaluate() -> None:
    """
    - Load raw data from local repository
    - Clean and preprocess data
    - Train a Random Forest Classifier
    - Save the pipeline locally
    - Evaluate the model on the test set
    """

    print(Fore.MAGENTA +
          "\n ⭐️ Use case: preprocess, train and evaluate" + Style.RESET_ALL)

    # Load raw data from local repository
    df = load_data()

    # Create X and y
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


def pred(X_pred: pd.DataFrame | None = None) -> list:
    '''
    - Load latest pipeline from local registry
    - Make predictions on new data
    Return predictions as a numpy array
    '''
    print(Fore.MAGENTA + "\n ⭐️ Use case: pred" + Style.RESET_ALL)

    if X_pred is None:
        X_pred = pd.DataFrame([['Male',
                                80.0, 0, 0,
                                'Yes', 'Govt_job',
                                'Urban', 148.72, 28.7,
                                'never smoked']],
                              columns=COLUMN_NAMES_RAW)

    pipeline = load_pipeline()
    y_pred = pipeline.predict(X_pred)

    res = list(map(lambda x: "Stroke" if x == 1 else "No Stroke", y_pred))
    print(f"{res}")

    print(f"✅ pred() done")

    return res


if __name__ == '__main__':
    try:
        # preprocess_and_train()
        pred()
    except:
        import sys
        import traceback

        import ipdb
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
