import boto3
import pandas as pd
import os


def execute_amazon():
    # load samples and credentials
    cwd = os.getcwd()
    texts_sample_fpath = os.path.join(cwd, 'data//texts_samples.csv')
    amazon_credentials_fpath = os.path.join(cwd, 'credentials//my_amazon_credentials.csv')
    amazon_credentials = retrieve_amazon_credentials(amazon_credentials_fpath)
    texts_df = pd.read_csv(texts_sample_fpath)

    # create amazon client
    aws_client = run_amazon_client(ACCESS_ID = amazon_credentials['Access key ID'],
                                   ACCESS_KEY = amazon_credentials['Secret access key'])

    # adapt format for amazon ingestion
    tweets_dicts = texts_df.to_dict(orient='records')

    #run loop for individual sentiment analysis and gather results in a list
    results_amazon = []
    for idx, tweet_dict in enumerate(tweets_dicts):
        sentiment, sentiment_score = get_amazon_sentiment(tweet_dict['text'], aws_client)
        print("Sentiment {} for {} / {}".format(sentiment, idx+1, len(tweets_dicts)))
        iter_dict = {
            "id": tweet_dict['id'],
            "aws_sentiment": sentiment,
            "aws_positive": sentiment_score['Positive'],
            "aws_negative": sentiment_score['Negative'],
            "aws_neutral": sentiment_score['Neutral'],
            "aws_mixed": sentiment_score['Mixed']
        }
        results_amazon.append(iter_dict)

    results_df = pd.DataFrame.from_dict(results_amazon)
    results_df.to_csv(os.path.join(cwd, 'results//amazon_sentiment.csv'), index=False)

    # Delete your amazon credentials, from local and on the cloud. This was just for fun.
    return results_df


def run_amazon_client(ACCESS_ID, ACCESS_KEY):
    return boto3.client(
        service_name='comprehend',
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=ACCESS_KEY,
        region_name='eu-west-1')


def get_amazon_sentiment(tweet, aws_client):
    aws_response = aws_client.detect_sentiment(Text=tweet, LanguageCode='es')
    return aws_response['Sentiment'], aws_response['SentimentScore']


def retrieve_amazon_credentials(fpath):
    creds_df = pd.read_csv(fpath)
    creds_dict = creds_df.to_dict(orient='records')

    return creds_dict[0]

    
if __name__ == '__main__':
    results = execute_amazon()
    print(results)
