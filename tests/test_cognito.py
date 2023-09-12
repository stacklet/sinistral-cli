# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import tempfile

from unittest import TestCase
from unittest.mock import Mock

import boto3
from click.testing import CliRunner
from moto import mock_cognitoidp
from stacklet.client.sinistral.cli import cli
from stacklet.client.sinistral.cognito import CognitoUserManager
from stacklet.client.sinistral.config import StackletConfig
from stacklet.client.sinistral.context import StackletContext


class CognitoUserManagerTest(TestCase):
    runner = CliRunner()
    cli = cli

    mock_cognitoidp = mock_cognitoidp()
    region = "us-east-1"

    def setUp(self):
        self.mock_cognitoidp.start()
        self.client = boto3.client("cognito-idp", region_name=self.region)
        resp = self.client.create_user_pool(PoolName="stackpool")
        self.cognito_user_pool_id = resp["UserPool"]["Id"]

        resp = self.client.create_user_pool_client(
            UserPoolId=self.cognito_user_pool_id, ClientName="stackpool-client"
        )
        self.cognito_client_id = resp["UserPoolClient"]["ClientId"]

    def tearDown(self):
        self.mock_cognitoidp.stop()

    def test_cognito_user_manager_create_user(self):
        config_data = dict(
            api="mock://stacklet.acme.org/api",
            cognito_user_pool_id=self.cognito_user_pool_id,
            cognito_client_id=self.cognito_client_id,
            region=self.region,
        )
        with tempfile.TemporaryDirectory() as temp:
            config = StackletConfig(temp)
            config.update(config_data)
            ctx = Mock(
                obj={
                    "output": "yaml",
                    "formatter": None,
                    "config": config,
                }
            )
        users = self.client.list_users(UserPoolId=self.cognito_user_pool_id)
        self.assertEqual(len(users["Users"]), 0)

        with StackletContext(ctx) as context:
            manager = CognitoUserManager.from_context(context)
            manager.create_user(
                user="test-user",
                password="Foobar123!",
                email="foo@acme.org",
                phone_number="+15551234567",
            )
            users = self.client.list_users(UserPoolId=self.cognito_user_pool_id)
            self.assertEqual(users["Users"][0]["Username"], "test-user")

            # creating a user is an idempotent action, this should return true without
            # raising an error
            res = manager.create_user(
                user="test-user",
                password="Foobar123!",
                email="foo@acme.org",
                phone_number="+15551234567",
            )
            self.assertTrue(res)
            users = self.client.list_users(UserPoolId=self.cognito_user_pool_id)
            self.assertEqual(users["Users"][0]["Username"], "test-user")
