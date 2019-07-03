
import urllib
import http
import json
import pandas as pd
import os

def get_azure_sentiment(texts_lists, AZURE_KEY):
    headers = {'Content-Type': 'application/json',
               'Ocp-Apim-Subscription-Key': f'{AZURE_KEY}'}
    params = urllib.parse.urlencode({'showStats': '{boolean}'})

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.1/sentiment?%s" % params,
                     f"{json.dumps(texts_lists)}",
                     headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return json.loads(data.decode('utf-8'))

def retrieve_azure_key_from_save_place(fpath):
    with open(fpath, "r") as f:
        my_azure_key = f.read()

    return my_azure_key

if __name__ == '__main__':

    cwd = os.getcwd()
    texts_sample_fpath = os.path.join(cwd, 'data//texts_samples.csv')
    azure_credentials_fpath = os.path.join(cwd, 'credentials//azure_key.txt')
    texts_df = pd.read_csv(texts_sample_fpath)

    #adapt to azure ingestion format
    texts_list_raw = texts_df.to_dict(orient='records')
    texts_list = {"documents": texts_list_raw}

    #retrieve azure key from saved plain txt file
    AZURE_KEY = retrieve_azure_key_from_save_place(azure_credentials_fpath)

    #call azure through rest API and get sentiment score
    sentiments = get_azure_sentiment(texts_list , AZURE_KEY)

    #adapt response format and merge with original dataframe
    sentiments_df = pd.DataFrame(sentiments['documents'])
    sentiments_df['id'] = sentiments_df['id'].astype(int)
    sentiments_df.rename(columns={'score':'azure_score'}, inplace=True)
    results_df = pd.merge(texts_df, sentiments_df, on='id')

    #show azure results
    print(results_df)

    #save azure results
    col_order = ['id', 'azure_score']
    results_df[col_order].to_csv(os.path.join(cwd, 'results//azure_sentiment.csv'), index=False)

    #Delete your azure txt credentials files from local and on the cloud. This was just for fun.