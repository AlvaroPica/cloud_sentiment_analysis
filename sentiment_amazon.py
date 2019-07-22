import boto3

import crosscutting as cc
from sentiment_executor import execute_cloud_sentiment


def execute_amazon():
    return execute_cloud_sentiment(
        'amazon_sentiment.csv',
        get_amazon_data,
        sentiment_field='aws_sentiment',
    )


def get_amazon_data(texts_list_raw):
    aws_client = get_amazon_client()
    return list(map(
        lambda tweet_dict: get_amazon_item_data(aws_client, tweet_dict),
        texts_list_raw
    ))


def get_amazon_item_data(aws_client, tweet_dict):
    aws_response = aws_client.detect_sentiment(Text=tweet_dict, LanguageCode='es')
    sentiment_score = aws_response['SentimentScore']

    return {
        'id': tweet_dict['id'],
        'aws_sentiment': aws_response['Sentiment'],
        'aws_positive': sentiment_score['Positive'],
        'aws_negative': sentiment_score['Negative'],
        'aws_neutral': sentiment_score['Neutral'],
        'aws_mixed': sentiment_score['Mixed']
    }


def get_amazon_client():
    amazon_credentials_fpath = cc.pathjoin('credentials', 'my_amazon_credentials.csv')
    amazon_credentials = cc.csv_load(amazon_credentials_fpath)[0]
    # Delete your amazon credentials, from local and on the cloud. This was just for fun.

    # create amazon client
    return boto3.client(
        service_name='comprehend',
        aws_access_key_id=amazon_credentials['Access key ID'],
        aws_secret_access_key=amazon_credentials['Secret access key'],
        region_name='eu-west-1'
    )


if __name__ == '__main__':
    results = execute_amazon()
    print(results)
