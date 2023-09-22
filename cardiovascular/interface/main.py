from data import load_data
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from pipeline import build_pipeline
from colorama import Fore, Style


def age_process(x):
    '''
    Function created to help the preprocessing of the age category feature
    '''
    if x in ['25-29', '18-24', '30-34']:
        return 'young'
    elif x in ['35-39', '40-44', '45-49', '50-54', '55-59']:
        return 'adult'
    else:
        return 'old'

def preprocess_and_train():
    data = load_data()
    data.drop_duplicates(inplace=True)

    data['age_category'] = data['Age_Category'].map(lambda x : age_process(x))
    data.drop(columns=['Age_Category', 'Checkup', 'BMI'], inplace=True)


    data.drop_duplicates(inplace=True)

    data['age_category'] = data['Age_Category'].map(lambda x : age_process(x))
    data.drop(columns=['Age_Category', 'Checkup', 'BMI'], inplace=True)

    X = data.drop(columns=['Heart_Disease'],axis=1)
    y = data[['Heart_Disease']]
    y_encoded =  OneHotEncoder(drop='if_binary', sparse=False, handle_unknown='ignore').fit_transform(y)
    X_train, _, y_train, _ = train_test_split(X,  # independent variables
                                              y_encoded,  # dependent variable
                                              test_size=0.2)
    # Build pipeline
    pipeline = build_pipeline()

    # Fit pipeline
    pipeline.fit(X_train, y_train)
    return pipeline

def evaluate():

    data = load_data()
    X = data.drop(columns=['Heart_Disease'],axis=1)
    y = data[['Heart_Disease']]
    y_encoded =  OneHotEncoder(drop='if_binary', sparse=False, handle_unknown='ignore').fit_transform(y)

    pipeline = build_pipeline()
    # Score model - accuracy
    accuracy = pipeline.score(X, y_encoded)
    print(f"✅ Model acurracy: {accuracy}")

def pred(X_pred: pd.DataFrame | None = None)->list:

    print(Fore.MAGENTA + "\n ⭐️ Use case: pred" + Style.RESET_ALL)
    pipeline = preprocess_and_train()
    return pipeline.predict(X_pred)



if __name__ == '__main__':
    preprocess_and_train()
    evaluate()
    pred()
