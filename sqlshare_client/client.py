from sqlshare_client.oauth import OAuth
from sqlshare_client.datasets import Datasets


class Client(object):
    def __init__(self, oauth_id, oauth_secret, server=None, redirect_uri=None):
        self.oauth = OAuth(oauth_id, oauth_secret, server, redirect_uri)

    def has_access(self):
        return self.oauth.has_access()

    def get_authorize_url(self):
        return self.oauth.get_authorize_url()

    def get_tokens_for_code(self, code):
        return self.oauth.request_token(code)

    def get_my_datasets(self):
        return Datasets(self.oauth).mine()

    def get_shared_datasets(self):
        return Datasets(self.oauth).shared()

    def get_all_datasets(self):
        return Datasets(self.oauth).all()

    def get_dataset(self, owner, name):
        return Datasets(self.oauth).get(owner, name)
