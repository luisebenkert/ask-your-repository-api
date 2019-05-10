from application.artifacts.artifact import Artifact
from application.artifacts.artifact_connector import ArtifactConnector


class ArtifactFactory:
    @classmethod
    def create_artifact(cls, user_tags=[], *args, **kwargs):
        artifact = cls.build_artifact(*args, **kwargs).save()

        if user_tags:
            builder = ArtifactConnector.for_artifact(artifact)
            builder.update_with(user_tags=user_tags)

        return artifact

    @classmethod
    def build_artifact(cls, **kwargs):
        if "file_url" not in kwargs:
            kwargs["file_url"] = "abc"
        return Artifact(**kwargs)
