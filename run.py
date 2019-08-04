import sys

from sentiment_amazon import execute_amazon
from sentiment_azure import execute_azure
from sentiment_merge import merge
from sentiment_google import execute_google

amazon_arg = '--amazon'
azure_arg = '--azure'
google_arg = '--google'
merge_arg = '--merge'
all_arg = '--all'

execute_by_arg = {
    amazon_arg: execute_amazon,
    azure_arg: execute_azure,
    merge_arg: merge,
    google_arg: execute_google,
}


def run(args):
    all = len(args) == 1 or all_arg in args

    for arg, execute_fn in execute_by_arg.items():
        if all or arg in args:
            print(execute_fn.__name__)
            print('-' * len(execute_fn.__name__))
            print(execute_fn())
            print('\n')


if __name__ == '__main__':
    run(sys.argv)
