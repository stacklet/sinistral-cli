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
  "idp_id": "JumpCloud",
  "auth_url": "https://sso.jumpcloud.com/saml2/sinistral",
}
```

Login with a cognito user (SSO support coming soon):

```
$ sinistral login --username $USER --password $PASSWORD
```

Run your first command:

```
$ sinistral projects get
```
