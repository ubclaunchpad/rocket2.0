"""All necessary class initializations."""
import os
import pem
import random
import string

from app.controller.command import CommandParser
from app.controller.command.commands.token import TokenCommandConfig
from datetime import timedelta
from db import DBFacade
from db.dynamodb import DynamoDB
from interface.github import GithubInterface, DefaultGithubFactory
from interface.slack import Bot
from slack import WebClient
from app.controller.webhook.github import GitHubWebhookHandler
from app.controller.webhook.slack import SlackEventsHandler
from config import Config

from typing import Optional, cast


def make_command_parser(config: Config,
                        gh: Optional[GithubInterface] = None) \
        -> CommandParser:
    """
    Initialize and returns a :class:`CommandParser` object.

    :return: a new ``CommandParser`` object, freshly initialized
    """
    slack_api_token, slack_bot_channel = "", ""
    signing_key = ""
    if not config.testing:
        slack_api_token = config.slack_api_token
        github_auth_key = pem.parse_file(config.github_key_file)[0].as_text()
        github_app_id = config.github_app_id
        github_organization = config.github_org_name
        slack_bot_channel = config.slack_bot_channel
        gh = GithubInterface(DefaultGithubFactory(github_app_id,
                                                  github_auth_key),
                             github_organization)
        if os.path.isfile(config.github_key_file):
            signing_key = open(config.github_key_file).read()
        else:
            signing_key = create_signing_token()
            open(config.github_key_file, 'w+').write(signing_key)
    facade = DBFacade(DynamoDB(config))
    bot = Bot(WebClient(slack_api_token), slack_bot_channel)
    # TODO: make token config expiry configurable
    token_config = TokenCommandConfig(timedelta(days=7), signing_key)
    return CommandParser(facade, bot, cast(GithubInterface, gh), token_config)


def make_github_webhook_handler(config: Config) -> GitHubWebhookHandler:
    """
    Initialize a :class:`GitHubWebhookHandler` object.

    :return: a new ``GitHubWebhookHandler`` object, freshly initialized
    """
    facade = DBFacade(DynamoDB(config))
    return GitHubWebhookHandler(facade, config)


def make_slack_events_handler(config: Config) -> SlackEventsHandler:
    """
    Initialize a :class:`SlackEventsHandler` object.

    :return: a new ``SlackEventsHandler`` object, freshly initialized
    """
    facade = DBFacade(DynamoDB(config))
    bot = Bot(WebClient(config.slack_api_token), config.slack_bot_channel)
    return SlackEventsHandler(facade, bot)


def create_signing_token() -> str:
    """Create a new, random signing token."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(24))
