import pytest
import pandas as pd
import os.path
from mock import MagicMock

import sentiment_google

magnitudes_and_scores = [
    (1.5,0.7),
    (1.0,-0.3),
    (0.4,-0.4),
    (0.1,0.0),
    (3.3,0.1),
    (3.4,0.8),
    (1.3,0.4)
]


def get_tweet_analysis_mock(magnitude_and_scores):
    magnitude, score = magnitude_and_scores
    tweet_analysis_mock = MagicMock()
    tweet_analysis_mock.document_sentiment.magnitude = magnitude
    tweet_analysis_mock.document_sentiment.score = score

    return tweet_analysis_mock


def test_execute_google():
    # arrange
    sentiment_google.language = MagicMock()
    language_svc_client_mock = sentiment_google.language.LanguageServiceClient.return_value
    tweet_analysis_mocks = list(map(get_tweet_analysis_mock, magnitudes_and_scores))
    language_svc_client_mock.analyze_sentiment.side_effect = tweet_analysis_mocks
        
    expected = pd.read_csv(os.path.join("tests", "test_google_sentiment_expected.csv"))

    # act
    result = sentiment_google.execute_google()

    # assert
    pd.testing.assert_frame_equal(expected, result)
