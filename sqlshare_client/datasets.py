import json
from urllib import quote


class Datasets(object):
    def __init__(self, oauth):
        self.oauth = oauth

    def mine(self):
        data = self.oauth.request("/v3/db/dataset/")
        return self._build_dataset_list(data)

    def shared(self):
        data = self.oauth.request("/v3/db/dataset/shared")
        return self._build_dataset_list(data)

    def all(self):
        data = self.oauth.request("/v3/db/dataset/all")
        return self._build_dataset_list(data)

    def get(self, owner, name):
        data = self.oauth.request("/v3/db/dataset/%s/%s" % (quote(owner),
                                                            quote(name)))
        return Dataset(json.loads(data))

    def get_permissions(self, owner, name):
        uri = "/v3/db/dataset/%s/%s/permissions"
        data = self.oauth.request(uri % (quote(owner), quote(name)))

        return Permissions(json.loads(data))

    def set_is_public(self, owner, name):
        uri = "/v3/db/dataset/%s/%s"
        data = self.oauth.request(uri % (quote(owner), quote(name)),
                                  method="PATCH",
                                  body='{"is_public": true }')
        return data

    def set_is_private(self, owner, name):
        uri = "/v3/db/dataset/%s/%s"
        data = self.oauth.request(uri % (quote(owner), quote(name)),
                                  method="PATCH",
                                  body='{"is_public": false }')
        return data

    def remove_sharing(self, owner, name):
        return self._set_sharing(owner, name, is_shared=False, is_public=False,
                                 accounts=[])

    def set_sharing(self, owner, name, accounts):
        return self._set_sharing(owner, name, is_shared=True, is_public=False,
                                 accounts=accounts)

    def _set_sharing(self, owner, name, is_public, is_shared, accounts):
        uri = "/v3/db/dataset/%s/%s/permissions"

        permissions = json.dumps({"is_public": is_public,
                                  "is_shared": is_shared,
                                  "authlist": accounts})

        data = self.oauth.request(uri % (quote(owner), quote(name)),
                                  method="PUT",
                                  body=permissions)
        return data

    def create_from_sql(self, owner, name, sql, description, is_public):
        # Force a true type value to be a boolean
        if is_public:
            is_public = True
        else:
            is_public = False
        ds_data = {
            "sql_code": sql,
            "is_public": is_public,
            "description": description,
        }
        data = self.oauth.request("/v3/db/dataset/%s/%s" % (quote(owner),
                                                            quote(name)),
                                  method="PUT",
                                  body=json.dumps(ds_data))

        return Dataset(json.loads(data))

    def _build_dataset_list(self, data):
        data = json.loads(data)
        datasets = []
        for value in data:
            datasets.append(Dataset(value))

        return datasets


class Permissions(object):
    def __init__(self, data={}):
        for key in data:
            if key == "accounts":
                setattr(self, key, map(lambda x: x["login"], data[key]))
            else:
                setattr(self, key, data[key])


class Dataset(object):
    def __init__(self, data={}):
        for key in data:
            setattr(self, key, data[key])

    def __str__(self):
        return "Dataset %s/%s" % (self.owner, self.name)

    def __cmp__(self, other):
        if self.owner < other.owner:
            return -1
        elif self.owner > other.owner:
            return 1

        if self.name < other.name:
            return -1
        if self.name > other.name:
            return 1

        return 0
