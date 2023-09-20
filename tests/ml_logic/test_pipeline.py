from mediml.ml_logic.pipeline import build_pipeline


def test_stroke_pipeline_length() -> None:
    '''
    Given a stroke model
    When the pipeline is trained
    Then the length of the pipeline should be 3
    '''
    pipeline = build_pipeline()
    assert len(pipeline) == 3
