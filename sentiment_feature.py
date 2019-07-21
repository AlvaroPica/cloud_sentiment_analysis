import pandas as pd
import os

FILE_PATHS = [
    os.path.join("results","azure_sentiment.csv"),
    os.path.join("results","google_sentiment.csv"),
    os.path.join("results","amazon_sentiment.csv"),
    os.path.join("data","texts_samples.csv"),
]


def analyze():
    sentiment_df = load_data()
    round_float_cols(sentiment_df)
    return sentiment_df


def load_data():
    sentiment_df = None
    for file_path in FILE_PATHS:
        sentiment_df = read_and_merge_data(file_path, sentiment_df)

    return sentiment_df


def read_and_merge_data(file_path, df = None):
    data_df = pd.read_csv(file_path)
    if df is None:
        return data_df

    return df.merge(data_df, on='id', how='left')


def round_float_cols(df):
    float_cols = df.select_dtypes(include='float64').columns.tolist()
    df[float_cols] = df[float_cols].apply(lambda x: round(x, 2))


if __name__ == '__main__':
    data = analyze()
    print(data)
