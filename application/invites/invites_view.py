"""Handle requests on the team resource."""
from flask import abort
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource
from flask_jwt_extended import get_jwt_identity, jwt_required

from application.teams.team import Team
from application.teams.team_schema import TEAM_SCHEMA
from application.users.user import User
from .invites_validator import accept_invite_args


class InvitesView(MethodResource):
    """Controller for invite links."""

    @jwt_required
    @use_kwargs(accept_invite_args())
    @marshal_with(TEAM_SCHEMA)
    def post(self, **params):
        """Logic for adding a single team member"""
        user = User.find_by(id_=get_jwt_identity())
        team = Team.find_by(join_key=params["join_key"], force=False)

        if not team:
            return abort(404, "this invite link is not valid")
        if user in team.members:
            return abort(409, "user already in team")

        team.members.connect(user)
        return team
