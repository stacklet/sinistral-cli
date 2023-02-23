import logging

import requests


class RestExecutor:
    def __init__(self, context, token):
        self.context = context
        self.api = self.context.config.api
        self.token = token
        self.log = logging.getLogger("stacklet.client.sinistral.executor")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def get(self, path, params={}, json=None):
        return self.session.get(self.api + path, params=params)

    def post(self, path, params={}, json=None):
        return self.session.post(self.api + path, json=json, params=params)

    def put(self, path, params={}, json=None):
        return self.session.put(self.api + path, json=json, params=params)

    def delete(self, path, params={}, json=None):
        return self.session.delete(self.api + path, json=json, params=params)
