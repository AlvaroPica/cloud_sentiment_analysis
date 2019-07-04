###  Import essentials ###

import pandas as pd
import os
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def get_google_sentiment(tweet, client):
    document = types.Document(
        content=tweet,
        language='es',
        type=enums.Document.Type.PLAIN_TEXT)
    tweet_analysis = client.analyze_sentiment(document=document)
    emotion = round(tweet_analysis.document_sentiment.magnitude, 3)
    sentiment = round(tweet_analysis.document_sentiment.score, 3)

    return sentiment, emotion

def google_rescale(x):
        _min, _max = -1, 1
        return (x - _min) / (_max - _min)

if __name__ == '__main__':

    cwd = os.getcwd()
    texts_sample_fpath = os.path.join(cwd, 'data//texts_samples.csv')
    google_credentials_fpath = os.path.join(cwd, 'credentials//my_google_credentials.json')
    texts_df = pd.read_csv(texts_sample_fpath)

    # create google_clientimport os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=google_credentials_fpath
    gcp_client = language.LanguageServiceClient()

    # adapt format for google ingestion
    tweets_dicts = texts_df.to_dict(orient='records')

    #run loop for individual sentiment analysis and gather results in a list
    results_gcp = []
    for idx, tweet_dict in enumerate(tweets_dicts):
        sentiment, emotion = get_google_sentiment(tweet_dict['text'], gcp_client)
        print("Sentiment {} for {} / {}".format(sentiment, idx+1, len(tweets_dicts)))
        iter_dict = {
            "id": tweet_dict['id'],
            "google_score": sentiment,
            "google_emotion": emotion,
        }

        results_gcp.append(iter_dict)

    #gather results in a dataframe
    results_df = pd.DataFrame.from_dict(results_gcp)

    #add google score rescaled to same range than azure score for comparison
    results_df['google_scaled'] = results_df['google_score'].map(lambda x: google_rescale(x))

    #Save google results
    results_df.to_csv(os.path.join(cwd, 'results//google_sentiment.csv'), index=False)

    print(results_df)
    # Delete your google cloud platform json credentials file from local and on the cloud. This was just for fun.