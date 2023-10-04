# MediML: Intelligent Diagnosis and Prediction in Medicine

## Description

This project serves as the final endeavor for LeWagon's batch-1275 flex-time Data Science bootcamp. Within this project, we aim to harness the power of machine learning and neural networks to make intelligent predictions concerning cardiovascular diseases, diabetes, and pneumonia using patient data and medical images.

## Training Data

We utilize several datasets from Kaggle to train our models, each serving a unique purpose:

1. [Cardiovascular Diseases Risk Prediction Dataset](https://www.kaggle.com/datasets/alphiree/cardiovascular-diseases-risk-prediction-dataset): This dataset contains data relevant to cardiovascular disease risk prediction, essential for our cardiac health predictions.
2. [Diabetes Healthcare Comprehensive Dataset](https://www.kaggle.com/datasets/deependraverma13/diabetes-healthcare-comprehensive-dataset): The comprehensive diabetes dataset enables us to develop models for diabetes prediction.
3. [Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset): Stroke prediction is a crucial aspect of our project, and this dataset provides the necessary data.
4. [Heart Failure Prediction](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction): We use this dataset to create models for predicting heart failure.
5. [Chest X-ray Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia): This dataset contains chest X-ray images essential for pneumonia prediction.

## Getting started

To test the model locally, follow these steps:

1. Install all the necessary packages:

```sh
make reinstall_package
```

2. Create the `.env` file at the root of the project:

```sh
LOCAL_MLOPS_DIRECTORY=.mlops
ENVIRONMENT=development
```

3. Create the `.env.development` file at the root of the project:

```sh
PIPELINE_TARGET=local
```

4. Create the folders where the models and the metrics will be stored:

```sh
make reset_local_files
```

5. Download the data [Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset), and put the CSV file inside the folder `.mlops/data/raw`. Make sure to call the file `healthcare-dataset-stroke-data.csv`

6. Run the following command inside the directory to train, evaluate the model or make a prediction:

```sh
# To train the model
make run_preprocess_and_train

# To evaluate the model
make run_evaluate

# To make a prediction
make run_pred

# To run the API
make run_api
```

## Authors

- Ignacio Martinez
- Eduardo Domínguez
- Fabian Windhagen
- Idriss SAADALLAH
- Remi DERONZIER

Feel free to explore our project and the datasets to gain insights into our intelligent diagnosis and prediction system in the field of medicine.
