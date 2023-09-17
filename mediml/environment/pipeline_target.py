from enum import Enum

from mediml.environment.params import PIPELINE_TARGET


class PipelineTarget(Enum):
    local = 1
    gcs = 2


def get_pipeline_target() -> PipelineTarget:
    '''
    Get the pipeline target from the environment variable `PIPELINE_TARGET`
    '''
    if not PIPELINE_TARGET:
        raise ValueError(
            "PIPELINE_TARGET environment variable must be set to 'local' or 'gcs'")
    return PipelineTarget[PIPELINE_TARGET]
