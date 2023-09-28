import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_selector, ColumnTransformer
from sklearn.tree import DecisionTreeClassifier





def build_pipeline():
    '''
    Builds a pipeline for the Cardiovascular model
    '''

    #Numerical transformer
    num_columns = make_column_selector(dtype_exclude=['object']) # type: ignore

    #Categorical transformer
    General_Health_sorted = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
    age_category_sorted = ['young', 'adult', 'old']

    # Define your categorical and ordinal columns
    ord_cols = ['General_Health', 'age_category']
    cat_cols = ['Smoking_History', 'Exercise', 'Skin_Cancer', 'Other_Cancer', 'Depression', 'Diabetes', 'Arthritis', 'Sex']

    # Create a ColumnTransformer for preprocessing
    preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ('numerical',RobustScaler(),num_columns),
        ('ordinal', OrdinalEncoder(categories=[General_Health_sorted, age_category_sorted], handle_unknown='use_encoded_value', unknown_value=-1), ord_cols),
        ('onehot', OneHotEncoder(drop='if_binary', sparse=False, handle_unknown='ignore'), cat_cols)
    ])

    clf = DecisionTreeClassifier(max_depth=5, min_samples_split=2, min_samples_leaf=1)

    pipeline = make_pipeline(preprocessing_pipeline,clf)

    return pipeline
