import json


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
