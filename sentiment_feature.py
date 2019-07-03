#### Retrieve sentiment analysis from Azure Text Analysis API Tool ####

import pandas as pd
import os

if __name__ == '__main__':

    # Load results dataset
    cwd = os.getcwd()
    texts_df = pd.read_csv(os.path.join(cwd, "data///texts_samples.csv"))
    azure_df = pd.read_csv(os.path.join(cwd, "results/azure_sentiment.csv"))
    google_df = pd.read_csv(os.path.join(cwd, "results/google_sentiment.csv"))
    amazon_df = pd.read_csv(os.path.join(cwd, "results/amazon_sentiment.csv"))

    sentiment_df = azure_df.merge(google_df,
                                       on='id',
                                       how='left')
    sentiment_df = sentiment_df.merge(amazon_df,
                                       on='id',
                                       how='left')
    sentiment_df = sentiment_df.merge(texts_df,
                                       on='id',
                                       how='left')

    sentiment_df['azure_sentiment'] = sentiment_df['azure_sentiment']\
        .map(lambda x: round(float(x),2))
    sentiment_df['google_sentiment'] = sentiment_df['google_sentiment']\
        .map(lambda x: round(float(x),2))
    sentiment_df['google_emotion'] =sentiment_df['google_emotion']\
        .map(lambda x: round(float(x),2))

    fpath = os.path.join(cwd, "data//train.tsv//train.tsv")
