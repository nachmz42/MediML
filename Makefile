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


################### DATA SOURCES ACTIONS ################

# Data sources
ML_DIR=~/.mediml/mlops

reset_local_files:
	rm -rf ${ML_DIR}
	mkdir -p ${ML_DIR}/data/
	mkdir ${ML_DIR}/data/raw
	mkdir ${ML_DIR}/data/processed
	mkdir ${ML_DIR}/training_outputs
	mkdir ${ML_DIR}/training_outputs/metrics
	mkdir ${ML_DIR}/training_outputs/pipelines
	mkdir ${ML_DIR}/training_outputs/params

################### TESTS ####################

tests_ml_logic:
	@pytest tests/ml_logic/test_pipeline.py -v

tests_all: tests_ml_logic

################### GCP ####################

copy_app_to_compute_engine:
	@echo "Copying app to compute engine"
	@gcloud compute scp --recurse . $USER@${VM_NAME}:~/mediml-project

connect_to_compute_engine:
	@echo "Connecting to compute engine"
	@gcloud compute ssh ${VM_NAME}