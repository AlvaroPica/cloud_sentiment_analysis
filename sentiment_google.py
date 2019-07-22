from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import crosscutting as cc
from sentiment_executor import execute_cloud_sentiment


def execute_google():
    return execute_cloud_sentiment(
        'google_sentiment.csv',
        get_google_data,
        sentiment_field="google_score",
        column_order=["google_emotion", "google_score", "id", "google_scaled"]
    )


def get_google_data(texts_list_raw):
    gcp_client = get_google_client()
    return list(map(
        lambda tweet_dict: get_google_item_data(gcp_client, tweet_dict),
        texts_list_raw
    ))


def get_google_item_data(gcp_client, tweet_dict):
    document = types.Document(
        content=tweet_dict['text'],
        language='es',
        type=enums.Document.Type.PLAIN_TEXT
    )
    tweet_analysis = gcp_client.analyze_sentiment(document=document)
    emotion = round(tweet_analysis.document_sentiment.magnitude, 3)
    sentiment = round(tweet_analysis.document_sentiment.score, 3)
    
    return {
        "id": tweet_dict['id'],
        "google_score": sentiment,
        "google_emotion": emotion,
        #add google score rescaled to same range than azure score for comparison
        "google_scaled": google_rescale(sentiment),
    }


def get_google_client():
    google_credentials_fpath = cc.pathjoin('credentials', 'my_google_credentials.json')
    cc.set_environ("GOOGLE_APPLICATION_CREDENTIALS", google_credentials_fpath)
    # Delete your google cloud platform json credentials file from local and on the cloud. This was just for fun.
    return language.LanguageServiceClient()


def google_rescale(x):
    _min, _max = -1, 1
    return (x - _min) / (_max - _min)


if __name__ == '__main__':
    results = execute_google()
    print(results)
