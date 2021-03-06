"""Handle Slack events."""
import logging
from app.model import User
from db.facade import DBFacade
from interface.slack import Bot, SlackAPIError
from typing import Dict, Any


class SlackEventsHandler:
    """Encapsulate the handlers for all Slack events."""

    welcome = 'Welcome to UBC Launch Pad! Please type `/rocket user edit '\
        '--github $GITHUB_USERNAME` to add yourself to the GitHub '\
        'organization.'

    def __init__(self,
                 db_facade: DBFacade,
                 bot: Bot):
        """Initialize all the required interfaces."""
        self.__facade = db_facade
        self.__bot = bot

    def handle_team_join(self, event_data: Dict[str, Any]):
        """
        Handle the event of a new user joining the workspace.

        :param event_data: JSON event data
        """
        new_id = event_data["event"]["user"]["id"]
        new_user = User(new_id)
        self.__facade.store(new_user)
        try:
            self.__bot.send_dm(SlackEventsHandler.welcome, new_id)
            logging.info(f"{new_id} added to database - user notified")
        except SlackAPIError:
            logging.error(f"{new_id} added to database - user not notified")
