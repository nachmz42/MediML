import pandas as pd


def load_data():
    '''
    Load data from cardiovascular disease
    '''

    df = pd.read_csv('../raw_data/CVD_cleaned.csv')

    return df
