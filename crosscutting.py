import csv
import http
import json
import os
import pandas as pd
import urllib


pathjoin = os.path.join
urlencode = urllib.parse.urlencode
json_dumps = json.dumps
pandas_read_csv = pd.read_csv
pandas_df_to_dict = pd.DataFrame.from_dict


def set_environ(env_name, env_value):
    os.environ[env_name] = env_value
    

def open_read_file(file_path):
    return open(file_path, 'r')


def read_file(file_path):
    with open_read_file(file_path) as file:
        return file.read()


def csv_load(fpath):
    with open_read_file(fpath) as csvfile:
        return list(map(dict, csv.DictReader(csvfile)))


def decode_utf8_and_load_json(data):
    return json.loads(data.decode('utf-8'))


def http_request(server_url, action, path, request_data, headers):
    try:
        conn = http.client.HTTPSConnection(server_url)
        conn.request(action, path, request_data, headers)
        response = conn.getresponse()
        response_data = response.read()
        conn.close()

    except Exception as e:
        print('[Errno {0}] {1}'.format(e.errno, e.strerror))

    return response_data
