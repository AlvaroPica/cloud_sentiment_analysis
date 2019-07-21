#### Retrieve Results from the three clouds for comparison purposes ####

import pandas as pd
import os

def analyze():
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

    float_cols = sentiment_df.select_dtypes(include='float64').columns.tolist()
    sentiment_df[float_cols] = sentiment_df[float_cols].apply(lambda x: round(x, 2))

    return sentiment_df


if __name__ == '__main__':
    data = analyze()
    print(data)
