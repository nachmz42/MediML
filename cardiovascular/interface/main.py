
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from colorama import Fore, Style
from cardiovascular.ml_logic.registry import load_pipeline, save_pipeline, save_results
from cardiovascular.ml_logic.pipeline import build_pipeline
from cardiovascular.ml_logic.data import load_data

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

def preprocess(data):
    print(f"✅ Starting the preprocessing of the cardiovascular data")
    data.drop_duplicates(inplace=True)

    data['age_category'] = data['Age_Category'].map(lambda x : age_process(x))
    data.drop(columns=['Age_Category', 'Checkup', 'BMI'], inplace=True)


    data.drop_duplicates(inplace=True)

    X = data.drop(columns=['Heart_Disease'],axis=1)
    y = data[['Heart_Disease']]
    y =  OneHotEncoder(drop='if_binary', sparse=False, handle_unknown='ignore').fit_transform(y)

    print(f"✅ Ending the preprocessing of the cardiovascular data")

    return X, y

def preprocess_and_train():
    print(f"✅ Starting the training of the cardiovascular model")
    data = load_data()
    X,y = preprocess(data)
    X_train, _, y_train, _ = train_test_split(X,
                                              y,
                                              test_size=0.2)
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    save_pipeline(pipeline)
    print(f"✅ Cardiovascular model trained")

def evaluate():
    print(f"✅ Starting the evaluation of the cardiovascular model")
    data = load_data()
    pipeline = load_pipeline()
    X,y = preprocess(data)
    accuracy = pipeline.score(X, y)
    print(f"✅ Model acurracy: {accuracy}")

def pred(X_pred: pd.DataFrame | None = None)->list:

    print(Fore.MAGENTA + "\n ⭐️ Use case: pred" + Style.RESET_ALL)
    pipeline = load_pipeline()
    return pipeline.predict(X_pred)



if __name__ == '__main__':
    preprocess_and_train()
    evaluate()
    pred()
