import crosscutting as cc
from sentiment_executor import execute_cloud_sentiment


def execute_azure():
    return execute_cloud_sentiment(
        'azure_sentiment.csv',
        get_azure_data,
        sentiment_field="azure_score",
        cols_to_save=['id','azure_score'],
        column_order=['id','text','language','azure_score'],
    )


def get_azure_data(texts_list_raw):
    azure_key = cc.read_file(cc.pathjoin('credentials', 'azure_key.txt'))
    raw_data = get_azure_sentiment(texts_list_raw, azure_key)
    return map_azure_raw_data(raw_data, texts_list_raw)


def get_azure_sentiment(texts_list_raw, azure_key):
    server_url = 'westeurope.api.cognitive.microsoft.com'
    request_data = cc.json_dumps({"documents": texts_list_raw})
    action='POST'
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': azure_key
    }
    params = cc.urlencode({'showStats': '{boolean}'})
    path = f'/text/analytics/v2.1/sentiment?{params}'
    
    response_data = cc.http_request(server_url, action, path, request_data, headers)

    return cc.decode_utf8_and_load_json(response_data)['documents']


def map_azure_raw_data(azure_raw_data, texts_list_raw):
    return [
        map_azure_data_item(azure_data_item, text)
        for azure_data_item, text in zip(azure_raw_data, texts_list_raw)
    ]


def map_azure_data_item(azure_data_item, text):
    return {
        "id": int(azure_data_item['id']),
        "text": text['text'],
        "language": text['language'],
        "azure_score": azure_data_item['azure_score'],
    }


if __name__ == '__main__':
    results = execute_azure()
    print(results)
