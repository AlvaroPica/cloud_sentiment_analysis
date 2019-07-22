import config
import crosscutting as cc
from sentiment_amazon import amazon_filename
from sentiment_azure import azure_filename
from sentiment_google import google_filename

FILE_PATHS = [
    cc.pathjoin(config.results_path, azure_filename),
    cc.pathjoin(config.results_path, google_filename),
    cc.pathjoin(config.results_path, amazon_filename),
    cc.pathjoin(config.data_path, config.input_filename),
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
