"""Test Github class."""
from github import Github, Organization, NamedUser, \
    GithubException, Team, GithubObject, PaginatedList
from interface.github import GithubInterface, GithubAPIException
from unittest import TestCase
from unittest.mock import MagicMock, Mock


class TestGithubInterface(TestCase):
    """Test case for GithubInterface class."""

    def setUp(self):
        """Set up testing environment."""
        self.mock_github = MagicMock(Github)
        self.mock_factory = MagicMock()
        self.mock_factory.create.return_value = self.mock_github
        self.mock_org = MagicMock(Organization.Organization)
        self.mock_github.get_organization.return_value = self.mock_org
        self.test_interface = GithubInterface(self.mock_factory,
                                              "ubclaunchpad")

        # make mock team
        self.mock_team = mock.MagicMock(Team.Team)

        self.mock_github.get_team = mock.MagicMock(side_effect={
            'brussels-sprouts': self.mock_team,
        }.get)

        self.test_user = mock.MagicMock(NamedUser.NamedUser)
        self.test_user.name = 'member_username'
        self.mock_team.get_members = mock.MagicMock(
                                        return_value=[self.test_user])

    def test_org_add_member(self):
        """Test GithubInterface method org_add_member."""
        mock_user: MagicMock = MagicMock(NamedUser.NamedUser)
        self.mock_github.get_user.return_value = mock_user
        self.test_interface.org_add_member("user@email.com")
        self.mock_org.add_to_members. \
            assert_called_once_with(mock_user, "member")

    def test_org_add_admin(self):
        """Test GithubInterface method org_add_admin."""
        mock_user: MagicMock = MagicMock(NamedUser.NamedUser)
        self.mock_github.get_user.return_value = mock_user
        self.test_interface.org_add_admin("user@email.com")
        self.mock_org.add_to_members. \
            assert_called_once_with(mock_user, "admin")

    def test_org_remove_member(self):
        """Test Github method org_remove_member."""
        mock_user: MagicMock = MagicMock(NamedUser.NamedUser)
        self.mock_github.get_user.return_value = mock_user
        self.test_interface.org_remove_member("user@email.com")
        self.mock_org.remove_from_membership.assert_called_once_with(mock_user)

    def test_org_has_member(self):
        """Test GithubInterface method org_has_member."""
        mock_user: MagicMock = MagicMock(NamedUser.NamedUser)
        self.mock_github.get_user.return_value = mock_user
        self.test_interface.org_has_member("user@email.com")
        self.mock_org.has_in_members.assert_called_once_with(mock_user)

    def test_org_get_team(self):
        """Test GithubInterface method org_get_team."""
        mock_team: MagicMock = MagicMock(Team.Team)
        self.mock_org.get_team.return_value = mock_team
        self.assertEqual(self.test_interface.org_get_team(2321313), mock_team)
        self.mock_org.get_team.assert_called_once_with(2321313)

    def test_org_create_team(self):
        """Test GithubInterface method org_create_team."""
        mock_team = Mock(id=234111)
        self.mock_org.create_team.return_value = mock_team
        self.assertEqual(
            self.test_interface.org_create_team("brussel sprouts"),
            234111)
        self.mock_org.create_team. \
            assert_called_once_with("brussel sprouts",
                                    GithubObject.NotSet, "closed", "push")

    def test_org_delete_team(self):
        """Test GithubInterface method org_delete_team."""
        mock_team = Mock(id=234111)
        self.mock_org.get_team.return_value = mock_team
        self.test_interface.org_delete_team(234111)
        self.mock_org.get_team.assert_called_once_with(234111)
        mock_team.delete.assert_called()

    def test_org_edit_team(self):
        """Test GithubInterface method org_edit_team."""
        mock_team: MagicMock = MagicMock(Team.Team)
        self.mock_org.get_team.return_value = mock_team
        self.test_interface.org_edit_team(234111, "brussels", "web team")
        self.mock_org.get_team.assert_called_once_with(234111)
        mock_team.edit.assert_called_once_with("brussels", "web team")

    def test_org_edit_team_name_only(self):
        """Test GithubInterface method org_edit_team with name only."""
        mock_team: MagicMock = MagicMock(Team.Team)
        self.mock_org.get_team.return_value = mock_team
        self.test_interface.org_edit_team(234111, "brussels")
        self.mock_org.get_team.assert_called_once_with(234111)
        mock_team.edit.assert_called_once_with("brussels")

    def test_org_get_teams(self):
        """Test GithubInterface method org_get_teams."""
        mock_list: MagicMock = MagicMock(PaginatedList.PaginatedList)
        self.mock_org.get_teams.return_value = mock_list
        self.test_interface.org_get_teams()
        self.mock_org.get_teams.assert_called_once()

    def test_setup_exception(self):
        """Test GithubInterface setup with exception raised."""
        self.mock_github. \
            get_organization.side_effect = GithubException("status", "data")
        try:
            test_bot = GithubInterface(self.mock_factory, "ubclaunchpad")
            assert False
        except GithubAPIException as e:
            pass

    def test_org_add_member_exception(self):
        """Test GithubInterface method org_add_member with exception raised."""
        self.mock_org.add_to_members. \
            side_effect = GithubException("status", "data")
        try:
            mock_user: MagicMock = MagicMock(NamedUser.NamedUser)
            self.mock_github.get_user.return_value = mock_user
            self.test_interface.org_add_member("user@email.com")
            assert False
        except GithubAPIException as e:
            pass

    def test_org_add_admin_exception(self):
        """Test GithubInterface method org_add_admin with exception raised."""
        self.mock_org.add_to_members. \
            side_effect = GithubException("status", "data")
        try:
            mock_user: MagicMock = MagicMock(NamedUser.NamedUser)
            self.mock_github.get_user.return_value = mock_user
            self.test_interface.org_add_admin("user@email.com")
            assert False
        except GithubAPIException as e:
            pass

    def test_org_remove_member_exception(self):
        """Test GithubInterface org_remove_member with exception raised."""
        self.mock_org.remove_from_membership. \
            side_effect = GithubException("status", "data")
        try:
            mock_user: MagicMock = MagicMock(NamedUser.NamedUser)
            self.mock_github.get_user.return_value = mock_user
            self.test_interface.org_remove_member("user@email.com")
            assert False
        except GithubAPIException as e:
            pass

    def test_org_has_member_exception(self):
        """Test GithubInterface method org_has_member with exception raised."""
        self.mock_org.has_in_members. \
            side_effect = GithubException("status", "data")
        try:
            mock_user: MagicMock = MagicMock(NamedUser.NamedUser)
            self.mock_github.get_user.return_value = mock_user
            self.test_interface.org_has_member("user@email.com")
            assert False
        except GithubAPIException as e:
            pass

    def test_org_get_team_exception(self):
        """Test GithubInterface method org_get_team with exception raised."""
        self.mock_org.get_team.side_effect = GithubException("status", "data")
        try:
            self.test_interface.org_get_team(2321313)
            assert False
        except GithubAPIException as e:
            pass

    def test_org_create_team_exception(self):
        """Test GithubInterface method org_create_team w/ exception raised."""
        self.mock_org.create_team. \
            side_effect = GithubException("status", "data")
        try:
            self.test_interface.org_create_team("brussel sprouts")
            assert False
        except GithubAPIException as e:
            pass

    def test_org_delete_team_exception(self):
        """Test GithubInterface method org_delete_team w/ exception raised."""
        try:
            mock_team = Mock(id=234111)
            self.mock_org.get_team.return_value = mock_team
            mock_team.delete. \
                side_effect = GithubException("status", "data")
            self.test_interface.org_delete_team(234111)
            assert False
        except GithubAPIException as e:
            pass

    def test_org_edit_team_exception(self):
        """Test GithubInterface method org_edit_team with exception raised."""
        try:
            mock_team: MagicMock = MagicMock(Team.Team)
            mock_team.edit.side_effect = GithubException("status", "data")
            self.mock_org.get_team.return_value = mock_team
            self.test_interface.org_edit_team(234111, "brussels", "web team")
            assert False
        except GithubAPIException as e:
            pass

    def test_org_get_teams_exception(self):
        """Test GithubInterface method org_get_teams with exception raised."""
        self.mock_org.get_teams.side_effect = GithubException("status", "data")
        try:
            self.test_interface.org_get_teams()
            assert False
        except GithubAPIException as e:
            pass

# -------------------------------------------------------------
# --------------- Tests related to team members ---------------
# -------------------------------------------------------------

    def test_tmem_list_team_members(self):
        """Test if list_team_members returns the right team members."""
        test_team_members_list = [mock.MagicMock(
                                    NamedUser.NamedUser)]
        self.mock_team.list_team_members = mock.MagicMock(
                                            return_value=test_team_members_list
                                            )
        self.test_bot.list_team_members('brussels-sprouts')
        self.mock_github.get_team.assert_called_once_with('brussels-sprouts')

    def test_tmem_get_team_member(self):
        """Test if method gets the correct member when member exists."""
        assert self.test_bot.\
            get_team_member(
                self.test_user.name, 'brussels-sprouts') is self.test_user

    def test_tmem_get_nonexistent_team_member(self):
        """Test if raises GithubException when memeber does not exist."""
        with self.assertRaises(GithubAPIException):
            self.test_bot.\
                    get_team_member(
                        'inexistent_username', 'brussels-sprouts')

    def test_tmem_add_team_member(self):
        """Test if a user is added to a team properly."""
        self.mock_github.get_user = mock.MagicMock(return_value=self.test_user)
        self.mock_team.add_membership = mock.MagicMock()

        self.test_bot.add_team_member('member_username', 'brussels-sprouts')
        self.mock_team.add_membership.assert_called_once_with(self.test_user)

    def test_tmem_remove_team_member(self):
        """Test if the user removed is no longer in the team."""
        self.mock_team.remove_membership = mock.MagicMock()
        self.mock_github.get_user = mock.MagicMock(return_value=self.test_user)
        self.test_bot.remove_team_member(
            self.test_user.name, 'brussels-sprouts')
        self.mock_team.remove_membership.assert_called_once_with(
                                                        self.test_user)
