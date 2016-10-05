from sqlshare_client import Client
from sqlshare_client.util.command_line import get_oauth_values
from tabulate import tabulate
import sys


def get_client(parser=None):
    data = get_oauth_values(parser)

    if 'id' not in data:
        print "Error: You need to specify a credentials path."
        raise Exception("Unconfigured")

    return Client(oauth_id=data['id'],
                  oauth_secret=data['secret'],
                  server=data['server'],
                  redirect_uri=data['redirect_uri'])


def list_datasets(datasets):
    for ds in sorted(datasets):
        print "%s/%s - %s" % (ds.owner, ds.name, ds.url)


def dump_dataset(dataset):
    for key in sorted(dir(dataset)):
        if not key.startswith('__'):
            print "%s: %s" % (key, getattr(dataset, key))


def display_query(query):
    if query.error:
        print "Error running query: %s" % (query.error)
        return

    print tabulate(query.sample_data, headers=query.columns)
