import pytest
import pandas as pd
import os.path
from mock import MagicMock

import sentiment_amazon


mock_data_list = [
    (0.07009565830230713,0.0008921491098590195,0.09940413385629654,0.8296080231666565,'POSITIVE'),
    (0.2226356565952301,0.5686514973640442,0.037764787673950195,0.17094801366329193,'NEGATIVE'),
    (0.030806897208094597,0.03816733881831169,0.8249551653862,0.10607059299945831,'NEUTRAL'),
    (0.009661787189543247,0.026334425434470177,0.8997037410736084,0.06430011987686157,'NEUTRAL'),
    (0.08932878822088242,0.0034786073956638575,0.08086888492107391,0.8263237476348877,'POSITIVE'),
    (0.10249777138233185,0.02760845050215721,0.11965476721525192,0.7502390146255493,'POSITIVE'),
    (0.14758895337581635,0.14615075290203094,0.47563424706459045,0.23062610626220703,'NEUTRAL'),
]


def get_tweet_analysis_mock(mock_data):
    aws_mixed,aws_negative,aws_neutral,aws_positive,aws_sentiment = mock_data
    tweet_analysis_mock = {
        'Sentiment': aws_sentiment,
        'SentimentScore': {
            'Positive': aws_positive,
            'Negative': aws_negative,
            'Neutral': aws_neutral,
            'Mixed': aws_mixed,
        }
    }

    return tweet_analysis_mock


def test_execute_amazon():
    # arrange
    sentiment_amazon.boto3 = MagicMock()
    amazon_client_mock = sentiment_amazon.boto3.client.return_value
    tweet_analysis_mocks = list(map(get_tweet_analysis_mock, mock_data_list))
    amazon_client_mock.detect_sentiment.side_effect = tweet_analysis_mocks

    expected = pd.read_csv(os.path.join('tests', 'test_amazon_sentiment_expected.csv'))

    # act
    result = sentiment_amazon.execute_amazon()

    # assert
    pd.testing.assert_frame_equal(expected, result)
    sentiment_amazon.boto3.client.assert_called_with(
        service_name='comprehend',
        aws_access_key_id='AKIA3GGJHW7FSUIBLCG3',
        aws_secret_access_key='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',
        region_name='eu-west-1',
    )
