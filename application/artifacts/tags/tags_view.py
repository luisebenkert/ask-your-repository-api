"""
Handles all logic of the artefacts api
"""
from flask import abort
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import fields, Schema

from application.errors import check_es_connection
from application.artifacts.artifact import Artifact
from application.teams.team import Team
from application.artifacts.artifact_connector import ArtifactConnector
from application.responders import no_content
from application.artifacts.tags import tag_suggestions, tags_validator


class SuggestedTagsSchema(Schema):
    """Schema for returning suggested tags"""

    tags = fields.List(fields.String())


class TagsView(MethodResource):
    """Controller for Artifacts"""

    method_decorators = [check_es_connection]

    @use_kwargs(tags_validator.add_tags_args())
    @marshal_with(None, 201)
    def add_tags(self, **params):
        """Adds tags to an existing artifact"""
        try:
            artifact = Artifact.find_by(id_=params.pop("id"))
            builder = ArtifactConnector.for_artifact(artifact)
            existing_tags = artifact.tags or []

            new_list = existing_tags + list(set(params["tags"]) - set(existing_tags))

            builder.update_with(tags=new_list)
            return no_content()
        except Artifact.DoesNotExist:
            return abort(404, "artifact not found")

    @use_kwargs(tags_validator.suggested_tags_args())
    @marshal_with(SuggestedTagsSchema)
    def suggested_tags(self, **params):
        """Takes an array of tags and suggests tags based on that"""
        current_tags = params["tags"]
        team = Team.find(params["team_id"])
        current_tags = [tag for tag in current_tags if tag != ""]
        return {"tags": tag_suggestions.find_tags(team, params["limit"], current_tags)}
