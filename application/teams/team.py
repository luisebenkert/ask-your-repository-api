"""Access to Team objects in Ne4J"""
import secrets
import string
from neomodel import StructuredNode, StringProperty, RelationshipTo, cardinality

from application.model_mixins import DefaultPropertyMixin, DefaultHelperMixin


def generate_join_key():
    while True:
        key = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        if not Team.find_by(join_key=key, force=False):
            break
    return key


class Team(StructuredNode, DefaultPropertyMixin, DefaultHelperMixin):
    """The class that manages Teams"""

    name = StringProperty(required=True)
    join_key = StringProperty(required=False, unique_index=True, default=generate_join_key)

    artifacts = RelationshipTo("application.models.Artifact", "UPLOADED", cardinality=cardinality.ZeroOrMore)
    members = RelationshipTo("application.models.User", "HAS_MEMBER", cardinality=cardinality.ZeroOrMore)
    drive_rel = RelationshipTo("application.models.Drive", "SYNCED_TO", cardinality=cardinality.ZeroOrOne)

    @property
    def drive(self):
        return self.drive_rel.single()
