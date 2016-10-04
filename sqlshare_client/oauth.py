from sanction import Client as SClient, transport_headers
from urllib2 import urlopen, HTTPError
import os
import json
DEFAULT_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
DEFAULT_SQLSHARE_SERVER = 'https://rest.sqlshare.uw.edu'


class OAuth(object):
    def __init__(self, oauth_id, oauth_secret, server=None, redirect_uri=None):
        self.oauth_id = oauth_id
        self.oauth_secret = oauth_secret
        if server is None:
            server = DEFAULT_SQLSHARE_SERVER

        if redirect_uri is None:
            redirect_uri = DEFAULT_REDIRECT_URI

        self.redirect_uri = redirect_uri
        client = SClient(auth_endpoint="%s/o/authorize/" % server,
                         token_endpoint="%s/o/token/" % server,
                         resource_endpoint="%s/v3" % server,
                         token_transport=transport_headers,
                         client_id=oauth_id,
                         client_secret=oauth_secret)

        self.server = server
        self.client = client
        self.access_token = None
        self.refresh_token = None

        self._load_config()

    def has_access(self):
        if self.access_token:
            return True
        return False

    def get_authorize_url(self):
        return self.client.auth_uri()
        self.request_token("oko")

    def request_token(self, code):
        token_request_data = {
            'code': code,
            'redirect_uri': self.redirect_uri,
        }

        self.client.request_token(**token_request_data)

        access_token = self.client.access_token
        refresh_token = self.client.refresh_token

        existing = self._read_config()

        existing[self.server] = {"access": access_token,
                                 "refresh": refresh_token
                                 }

        self.access_token = access_token
        self.refresh_token = refresh_token
        self._write_config(existing)

    def request(self, url, method="GET", input_body=None, headers={},
                is_reauth_attempt=False):
        client = self.client
        req = client.token_transport('{0}{1}'.format(self.server, url),
                                     self.access_token, data=input_body,
                                     method=method,
                                     headers=headers)

        try:
            resp = urlopen(req)
        except HTTPError as e:
            resp = e

        body = resp.read()
        if resp.getcode() == 403:
            if body.find("SQLShare: Access Denied") < 0:
                # Without the SQLShare error, assume an oauth issue.
                if not is_reauth_attempt:
                    c = self.client
                    refresh = self.refresh_token

                    c.request_token(grant_type='refresh_token',
                                    refresh_token=refresh)

                    new_data = self._load_config()
                    self.refresh_token = c.refresh_token
                    self.access_token = c.access_token

                    new_data[self.server]["access"] = self.access_token
                    new_data[self.server]["refresh"] = self.refresh_token

                    self._write_config(new_data)

                    return self.request(url, method, input_body, headers,
                                        is_reauth_attempt=True)

        return body

    def _get_path(self):
        return os.path.expanduser("~/.sqlshare-rest.cfg")

    def _read_config(self):
        data = ""
        path = self._get_path()
        fd = os.open(path, os.O_RDWR | os.O_APPEND | os.O_CREAT, 0o600)

        private_config = os.fdopen(fd, "rw")

        existing = {}
        with open(path, "r") as private_config:
            try:
                for line in private_config:
                    data += line

                existing = json.loads(data)

            except Exception as ex:
                existing = {}

        return existing

    def _write_config(self, data):
        path = self._get_path()

        with open(path, "w") as private_config:
            private_config.write(json.dumps(data)+"\n")

    def _load_config(self):
        data = self._read_config()
        if self.server in data:
            self.access_token = data[self.server]["access"]
            self.refresh_token = data[self.server]["refresh"]
        return data
