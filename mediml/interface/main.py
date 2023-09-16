from pathlib import Path

import pandas as pd
from colorama import Fore, Style
from sklearn.model_selection import train_test_split

from mediml.ml_logic.data import load_data
from mediml.ml_logic.pipeline import build_pipeline
from mediml.ml_logic.registry import load_pipeline, save_pipeline, save_results
from mediml.params import COLUMN_NAMES_RAW


def preprocess_and_train() -> None:
    """
    - Load raw data
    - Clean and preprocess data
    - Train a Random Forest Classifier
    - Save the pipeline
    """

    print(Fore.MAGENTA + "\n ⭐️ Use case: preprocess and train" + Style.RESET_ALL)

    # Load raw data from local repository
    df = load_data()

    # Create X and y
    X = df.drop("stroke", axis=1)
    y = df.stroke

    # Split into train & test set
    X_train, _, y_train, _ = train_test_split(X,  # independent variables
                                              y,  # dependent variable
                                              test_size=0.2)  # percentage of data to use for test set

    # Build pipeline
    pipeline = build_pipeline()

    # Fit pipeline
    pipeline.fit(X_train, y_train)

    # Save pipeline
    save_pipeline(pipeline=pipeline)


def evaluate() -> None:
    '''
    - Load latest pipeline
    - Evaluate the model on the test set
    '''

    print(Fore.MAGENTA + "\n⭐️ Use case: evaluate" + Style.RESET_ALL)

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

    # Build pipeline
    pipeline = load_pipeline()

    # Score model - accuracy
    acurracy = pipeline.score(X, y)
    print(f"✅ Model acurracy: {acurracy}")

    # Save metrics
    save_results(metrics={"accuracy": acurracy})


def pred(X_pred: pd.DataFrame | None = None) -> list:
    '''
    - Load latest pipeline
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
    preprocess_and_train()
    evaluate()
    pred()
