from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


def build_pipeline() -> Pipeline:
    """
    Builds a pipeline that preprocess the data and trains a model
    (RandomForestClassifier)
    """

    # Impute then scale numerical values
    num_transformer = make_pipeline(
        SimpleImputer(strategy="mean"), StandardScaler())
    num_col = make_column_selector(dtype_include=['float64'])  # type: ignore

    # Encode categorical values
    cat_transformer = OneHotEncoder(handle_unknown='ignore')
    # Add int64 in categorical values to include `heart_disease` and `hypertension`
    cat_col = make_column_selector(
        dtype_include=['object', 'bool', 'int64'])  # type: ignore

    # Parallelize "num_transformer" and "cat_transfomer"
    preprocessor = make_column_transformer(
        (num_transformer, num_col),
        (cat_transformer, cat_col),
        remainder='passthrough'
    )

    smt = SMOTE(random_state=42)

    model = RandomForestClassifier()

    pipeline = make_pipeline(preprocessor, smt, model)

    return pipeline
