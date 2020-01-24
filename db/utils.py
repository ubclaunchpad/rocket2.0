"""Database utilities, for functions that you use all the time."""
from db.facade import DBFacade
from app.model.team import Team
import logging


def get_team_by_name(dbf: DBFacade, gh_team_name: str) -> Team:
    """
    Query team by github team name.

    Can only return a single team. If there are no teams with that name, or
    there are multiple teams with that name, we raise an error.

    :raises: LookupError if the calling user, user to add,
             or specified team cannot be found in the database
    :raises: RuntimeError if more than one team has the specified
             team name
    :return: Team if found
    """
    teams = dbf.query(Team,
                      [('github_team_name', gh_team_name)])

    if len(teams) < 1:
        msg = f"No teams found with team name {gh_team_name}"
        logging.error(msg)
        raise LookupError(msg)
    elif len(teams) > 1:
        msg = f"{len(teams)} found with team name {gh_team_name}"
        logging.error(msg)
        raise RuntimeError(msg)
    else:
        logging.info(f"Team queried with team name {gh_team_name}:"
                     f" {teams[0].__str__()}")
        return teams[0]
