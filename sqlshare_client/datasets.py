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
