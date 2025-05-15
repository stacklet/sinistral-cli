# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging

import boto3
import requests


class CognitoUserManager:
    """
    Manage a cognito user
    """

    def __init__(
        self,
        user_pool_id,
        user_pool_client_id,
        region,
    ):
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.region = region
        self.client = boto3.client("cognito-idp", region_name=self.region)
        self.log = logging.getLogger("CognitoUserManager")

    @classmethod
    def from_context(cls, context):
        return cls(
            user_pool_id=context.config.cognito_user_pool_id,
            user_pool_client_id=context.config.cognito_client_id,
            region=context.config.cognito_region,
        )

    def create_user(self, user, password, email, phone_number, permanent=True):
        """
        Creates an admin cognito user with the default password out of the box
        """
        self.email = email
        self.phone_number = phone_number
        attrs = []
        if email:
            attrs.append({"Name": "email", "Value": email})
            attrs.append({"Name": "email_verified", "Value": "True"})
        if phone_number:
            attrs.append({"Name": "phone_number", "Value": phone_number})
            attrs.append({"Name": "phone_number_verified", "Value": "True"})
        try:
            res = self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=user,
                TemporaryPassword=password,
                UserAttributes=attrs,
                MessageAction="SUPPRESS",
                DesiredDeliveryMediums=["SMS", "EMAIL"],
            )
            self.log.debug(res)
        except self.client.exceptions.UsernameExistsException:
            self.log.debug("User:%s already exists. Resetting password." % user)

        if not permanent:
            return True

        # update the password so it's set permantently
        self.log.debug("Resetting admin password to disable temporary password for %s" % user)
        res = self.client.admin_set_user_password(
            UserPoolId=self.user_pool_id,
            Username=user,
            Password=password,
            Permanent=True,
        )
        self.log.debug(res)
        return True

    def login(self, user, password):
        res = self.client.initiate_auth(
            ClientId=self.user_pool_client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": user, "PASSWORD": password},
        )
        self.log.debug("Authentication Success")
        return res["AuthenticationResult"]["AccessToken"]


class CognitoClientAuth:
    """
    Manage Cognito client credentials based auth flow.
    """

    def __init__(self, ctx):
        self.ctx = ctx

    def get_access_token(self, auth_url, client_id, client_secret):
        response = requests.post(
            f"{auth_url}/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )
        if response.status_code != 200:
            self.ctx.fail(f"Unable to get access token:\n{response.text}")
        return response.json()["access_token"]
