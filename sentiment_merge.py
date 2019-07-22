import crosscutting as cc

FILE_PATHS = [
    cc.pathjoin('results','azure_sentiment.csv'),
    cc.pathjoin('results','google_sentiment.csv'),
    cc.pathjoin('results','amazon_sentiment.csv'),
    cc.pathjoin('data','texts_samples.csv'),
]


def merge():
    sentiment_df = load_data()
    round_float_cols(sentiment_df)
    return sentiment_df


def load_data():
    sentiment_df = None
    for file_path in FILE_PATHS:
        sentiment_df = read_and_merge_data(file_path, sentiment_df)

    return sentiment_df


def read_and_merge_data(file_path, df = None):
    data_df = cc.pandas_read_csv(file_path)
    if df is None:
        return data_df

    return df.merge(data_df, on='id', how='left')


def round_float_cols(df):
    float_cols = df.select_dtypes(include='float64').columns.tolist()
    df[float_cols] = df[float_cols].apply(lambda x: round(x, 2))


if __name__ == '__main__':
    data = merge()
    print(data)
