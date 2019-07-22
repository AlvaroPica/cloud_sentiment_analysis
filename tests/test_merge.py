import pytest
import pandas as pd
import os.path

from sentiment_merge import merge


# TODO because file write is not mocked, this test must be executed last
def test_merge():
    # arrange
    expected = pd.read_csv(os.path.join('tests', 'test_merge.csv'))

    # act
    result = merge()

    # assert
    pd.testing.assert_frame_equal(expected, result)
