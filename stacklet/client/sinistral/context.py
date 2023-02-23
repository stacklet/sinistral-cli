import os
from stacklet.client.sinistral.config import StackletConfig, DEFAULT_PATH


class StackletContext:
    """
    CLI Execution Context
    """

    DEFAULT_CONFIG = DEFAULT_PATH
    DEFAULT_CREDENTIALS = "~/.stacklet/sinistral/credentials"
    DEFAULT_ID = "~/.stacklet/sinistral/id"
    DEFAULT_OUTPUT = "yaml"

    def __init__(self, config=None, raw_config=None):
        if 'STACKLET_CONFIG' in os.environ:
            config = os.environ['STACKLET_CONFIG']
        if isinstance(raw_config, dict) and len(raw_config.values()) != 0:
            self.config = StackletConfig(**raw_config)
        elif config:
            self.config = StackletConfig.from_file(config)
        else:
            self.config = StackletConfig.from_file(self.DEFAULT_CONFIG)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return

    def can_sso_login(self):
        return all(
            [
                self.config.auth_url,
                self.config.cognito_client_id,
            ]
        )


class StackletCredentialWriter:
    def __init__(self, credentials, location=StackletContext.DEFAULT_CREDENTIALS):
        self.credentials = credentials
        self.location = location

    def __call__(self):
        if not os.path.exists(os.path.dirname(os.path.expanduser(self.location))):
            os.makedirs(os.path.dirname(os.path.expanduser(self.location)))
        with open(os.path.expanduser(self.location), "w+") as f:
            f.write(self.credentials)
