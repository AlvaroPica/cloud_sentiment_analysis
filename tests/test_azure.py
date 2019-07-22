import pytest
import pandas as pd
import os.path
from mock import MagicMock

import crosscutting as cc
import sentiment_azure


def test_execute_azure():
    # arrange
    mock_data_path = os.path.join('tests', 'test_azure_sentiment_mock_data.json')
    with open(mock_data_path) as json_file:
        http_call_response_data = json_file.read()

    cc.http = MagicMock()
    conn_mock = cc.http.client.HTTPSConnection.return_value
    response_mock = conn_mock.getresponse.return_value
    response_data_mock = response_mock.read.return_value
    response_data_mock.decode.return_value = http_call_response_data

    expected_request_data_path = os.path.join('tests', 'test_azure_sentiment_expected_request.json')
    with open(expected_request_data_path) as json_file:
        expected_request_data = json_file.read()
        
    expected = pd.read_csv(os.path.join("tests", "test_azure_sentiment_expected.csv"))

    # act
    result = sentiment_azure.execute_azure()

    # assert
    pd.testing.assert_frame_equal(expected, result)
    cc.http.client.HTTPSConnection.assert_called_with('westeurope.api.cognitive.microsoft.com')
    conn_mock.request.assert_called_with(
        'POST',
        '/text/analytics/v2.1/sentiment?showStats=%7Bboolean%7D',
        expected_request_data,
        {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '7f268b0fcb614170bacb832ae89e2164'
        }
    )
    conn_mock.getresponse.assert_called()
    conn_mock.close.assert_called()
