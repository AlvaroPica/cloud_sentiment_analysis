import config
import crosscutting as cc


def execute_cloud_sentiment(
    output_filename,
    get_cloud_data,
    sentiment_field,
    cols_to_save=None,
    column_order=None
):
    input_file_path = cc.pathjoin(config.data_path, config.input_filename)

    texts_df = cc.pandas_read_csv(input_file_path)
    texts_list_raw = texts_df.to_dict(orient='records')

    cloud_data = get_cloud_data(texts_list_raw)
    # TODO pandas not needed
    results_df = cc.pandas_df_to_dict (cloud_data)
    log_data(results_df, sentiment_field)

    if column_order:
        results_df = results_df[column_order]

    df_to_save = results_df if not cols_to_save else results_df[cols_to_save]
    output_file_path = cc.pathjoin(config.results_path, output_filename)
    df_to_save.to_csv(output_file_path, index=False)

    return results_df


def log_data(results_df, sentiment_field):
    total_items = results_df.shape[1]
    for idx, item_data in results_df.iterrows():
        print(f'Sentiment {item_data[sentiment_field]} for {idx+1} / {total_items}')
