import logging

import requests

from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.formatter import Formatter
from stacklet.client.sinistral.utils import get_token


class RestExecutor:
    def __init__(self, context, token):
        self.context = context
        self.api = self.context.config.api
        self.token = token
        self.log = logging.getLogger('stacklet.client.sinistral.executor')
        self.session = requests.Session()
        self.session.headers.update(
            {
                'Authorization': f'Bearer {self.token}'
            }
        )

    def get(self, path, json):
        return self.session.get(self.api + path)

    def post(self, path, json):
        return self.session.post(self.api + path, json=json)


def make_request(ctx, method, path, json={}):
    with StackletContext(ctx.obj["config"], ctx.obj["raw_config"]) as context:
        token = get_token()
        executor = RestExecutor(context, token)
        func = getattr(executor, method)
        res = func(path, json).json()
        fmt = Formatter.registry.get(ctx.obj["output"])()
    return fmt(res)
