from sqlshare_client import Client
from sqlshare_client.util.command_line import get_oauth_values
import sys


data = get_oauth_values()

c = Client(oauth_id=data['id'],
           oauth_secret=data['secret'],
           server=data['server'],
           redirect_uri=data['redirect_uri'])

if not c.has_access():
    print "Visit this url, and then enter the code below:"
    print c.get_authorize_url()

    code = sys.stdin.readline()[:-1]

    c.get_tokens_for_code(code=code)

datasets = c.get_my_datasets()
datasets = c.get_shared_datasets()
datasets = c.get_all_datasets()


print datasets[0]
