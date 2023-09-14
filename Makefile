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

tests_all:
	make tests_ml_logic