import pytest
import pandas as pd
import os.path

from sentiment_feature import analyze


def test_analyze():
    # arrange
    expected = pd.read_csv(os.path.join("tests", "test_analize.csv"))

    # act
    result = analyze()

    # assert
    pd.testing.assert_frame_equal(expected, result)
