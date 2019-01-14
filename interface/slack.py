"""Utility classes for interacting with Slack API."""
import logging


class Bot:
    """Utility class for calling Slack APIs."""

    def __init__(self, sc):
        """Initialize Bot by creating a SlackClient Object."""
        logging.info("Initializing Slack client interface")
        self.sc = sc

    def send_dm(self, message, slack_user_id):
        """Send direct message to user with id of slack_user_id."""
        logging.debug("Sending direct message to {}".format(slack_user_id))
        response = self.sc.api_call(
            "chat.postMessage",
            channel=slack_user_id,
            text=message
        )
        if 'ok' not in response:
            logging.error("Direct message to {} failed with error: {}".
                          format(slack_user_id, response['error']))
            raise SlackAPIError(response['error'])

    def send_to_channel(self, message, channel_name, attachments=[]):
        """Send message to channel with name channel_name."""
        logging.debug("Sending message to channel {}".format(channel_name))
        response = self.sc.api_call(
            "chat.postMessage",
            channel=channel_name,
            attachments=attachments,
            text=message
        )
        if 'ok' not in response:
            logging.error("Message to channel {} failed with error: {}".
                          format(channel_name, response['error']))
            raise SlackAPIError(response['error'])


class SlackAPIError(Exception):
    """Exception representing an error while calling Slack API."""

    def __init__(self, error):
        """
        Initialize a new SlackAPIError.

        :param error: Error string returned from Slack API.
        """
        self.error = error