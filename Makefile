.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################

# To understand the colon in POSIX makefiles, see https://www.ibm.com/docs/en/zos/2.4.0?topic=descriptions-colon-do-nothing-successfully
# The || : is to ignore the error if the package is not installed
# The -y flag is to automatically answer yes to the uninstall prompt
reinstall_package:
	@pip uninstall -y mediml || :
	@pip install -e .

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -f */.ipynb_checkpoints
	@rm -Rf build
	@rm -Rf */__pycache__
	@rm -Rf */*.pyc

run_preprocess_and_train:
	python -c 'from mediml.interface.main import preprocess_and_train; preprocess_and_train()'

run_pred:
	python -c 'from mediml.interface.main import pred; pred()'

run_evaluate:
	python -c 'from mediml.interface.main import evaluate; evaluate()'

run_all: run_preprocess_and_train run_pred run_evaluate

run_api:
	uvicorn mediml.api.fast:app --reload


################### DATA SOURCES ACTIONS ################

# Data sources
reset_local_files:
	rm -rf ${LOCAL_MLOPS_DIRECTORY}
	mkdir -p ${LOCAL_MLOPS_DIRECTORY}/data/
	mkdir ${LOCAL_MLOPS_DIRECTORY}/data/raw
	mkdir ${LOCAL_MLOPS_DIRECTORY}/data/processed
	mkdir ${LOCAL_MLOPS_DIRECTORY}/training_outputs
	mkdir ${LOCAL_MLOPS_DIRECTORY}/training_outputs/metrics
	mkdir ${LOCAL_MLOPS_DIRECTORY}/training_outputs/pipelines
	mkdir ${LOCAL_MLOPS_DIRECTORY}/training_outputs/params

################### TESTS ####################

tests_ml_logic:
	@pytest tests/ml_logic/test_pipeline.py -v

tests_all: tests_ml_logic

################### GCP COMPUTE ENGINE ####################

copy_app_to_compute_engine:
	@echo "Copying app to compute engine"
	@gcloud compute scp --recurse . ${VM_NAME}:~/mediml-project

connect_to_compute_engine:
	@echo "Connecting to compute engine"
	@gcloud compute ssh ${VM_NAME}

################### DOCKER ####################
TAG = latest # default TAG
DOCKER_GCP_IMAGE_FULL_NAME = ${GCP_MULTI_REGION}-docker.pkg.dev/${PROJECT}/${GCP_REGISTRY}/${DOCKER_GCP_IMAGE_NAME}

# Make sure to set the environment variables in .env to `development` before running this command
build_docker_image_local:
	@echo "Building docker image"
	@docker build -t ${DOCKER_LOCAL_IMAGE_NAME}:$(TAG) --build-arg GCP_CREDENTIALS_PATH=gcp-creds.json --build-arg BUCKET_NAME=${BUCKET_NAME} --build-arg LOCAL_MLOPS_DIRECTORY=${LOCAL_MLOPS_DIRECTORY} .

# Make sure to set the environment variables in .env to `production` before running this command
build_docker_image_gcp:
	@echo "Building docker image for GCP"
	@docker build --platform linux/amd64 -t ${DOCKER_GCP_IMAGE_FULL_NAME}:$(TAG) --build-arg GCP_CREDENTIALS_PATH=gcp-creds.json --build-arg BUCKET_NAME=${BUCKET_NAME} --build-arg LOCAL_MLOPS_DIRECTORY=${LOCAL_MLOPS_DIRECTORY} .

run_docker_api_local:
	@echo "Running docker api image locally"
	@docker run -it -e PORT=8000 -p 8000:8000 ${DOCKER_LOCAL_IMAGE_NAME}:$(TAG)

run_docker_api_gcp:
	@echo "Running docker api image to test GCP deployment"
	@docker run -it -e PORT=8000 -p 8000:8000 ${DOCKER_GCP_IMAGE_FULL_NAME}:$(TAG)

run_docker_shell_local:
	@echo "Running docker image shell locally"
	@docker run -it ${DOCKER_LOCAL_IMAGE_NAME}:$(TAG) sh

run_docker_shell_gcp:
	@echo "Running docker image shell to test GCP deployment"
	@docker run -it ${DOCKER_GCP_IMAGE_FULL_NAME}:$(TAG) sh

push_docker_image_gcp:
	@echo "Pushing docker image to GCP"
	@docker push ${DOCKER_GCP_IMAGE_FULL_NAME}:$(TAG)

################### DEPLOY ####################

deploy_docker_image_gcp:
	@echo "Deploying docker image to Cloud Run"
	@gcloud run deploy ${GCP_SERVICE_NAME} --image ${DOCKER_GCP_IMAGE_FULL_NAME}:$(TAG) --platform managed --region ${GCP_LOCAL_REGION}

################### FIREBASE HOSTING ####################

build_firebase_config_file:
	@echo "Building firebase config file"
	@python build_firebase_config.py

deploy_firebase_hosting:
	@echo "Deploying firebase hosting"
	@firebase deploy --only hosting --project ${PROJECT}