# Sinistral CLI

## Setup

```
$ poetry shell
$ poetry install
```

Create a config file at `~/.stacklet/sinistral/config.json`:

```json
{
  "api": "https://api.sinistral.stacklet.io",
  "region": "us-east-1",
  "cognito_client_id": "5bogrjv9om1tjhfsd1c8d2kouo",
  "cognito_user_pool_id": "us-east-1_F4Ca4BFQS",
  "idp_id": "idp-4a301a48-cd63-4c6c-caf7-419c5b0ee737",
  "auth_url": "https://auth.sinistral.stacklet.io"
}
```

Login with a cognito user:

```
$ sinistral login --username $USER --password $PASSWORD
```

Or, login with SSO:

```
$ sinistral login
```

Run your first command:

```
$ sinistral projects list
```

Python client:

```python
from stacklet.client.sinistral.client import sinistral_client

sinistral = sinistral_client()
policy_client = sinistral.client('policies')
print(policy_client.list())
```
