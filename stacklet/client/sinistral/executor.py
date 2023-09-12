# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging

import requests


class RestExecutor:
    def __init__(self, context, token):
        self.context = context
        self.api_url = self.context.config.api_url
        self.token = token
        self.log = logging.getLogger("stacklet.client.sinistral.executor")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def get(self, path, params={}, json=None):
        return self.session.get(self.api_url + path, params=params)

    def post(self, path, params={}, json=None):
        return self.session.post(self.api_url + path, json=json, params=params)

    def put(self, path, params={}, json=None):
        return self.session.put(self.api_url + path, json=json, params=params)

    def delete(self, path, params={}, json=None):
        return self.session.delete(self.api_url + path, json=json, params=params)
