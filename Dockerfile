FROM python:3.10.6-buster

WORKDIR /prod

# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...
COPY requirements_prod.txt requirements.txt
RUN pip install -r requirements.txt

ARG GCP_CREDENTIALS_PATH
ARG BUCKET_NAME
ARG LOCAL_MLOPS_DIRECTORY

# Copy GCP credentials to the container
COPY $GCP_CREDENTIALS_PATH gcp-creds.json

# Set the environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS=/prod/gcp-creds.json
ENV BUCKET_NAME=$BUCKET_NAME
ENV PIPELINE_TARGET="gcs"
ENV LOCAL_MLOPS_DIRECTORY=$LOCAL_MLOPS_DIRECTORY

COPY mediml mediml
COPY setup.py setup.py
RUN pip install .

COPY Makefile Makefile
RUN make reset_local_files

# Specify the port number the container should expose for GCP
CMD uvicorn mediml.api.fast:app --host 0.0.0.0 --port $PORT

