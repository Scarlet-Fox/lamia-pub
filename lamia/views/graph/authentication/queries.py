"""Queries associated with lamia authentication."""
# pylint: disable=unused-argument
import graphene
import pendulum
from graphql import GraphQLError
from lamia.views.graph.objecttypes import IdentityObjectType
from lamia.models.features import Identity
from lamia.models.activitypub import Actor
from lamia.config import BASE_URL


class IdentityQuery(graphene.ObjectType):
    """Returns an identity."""
    identity = graphene.Field(lambda: IdentityObjectType)

    async def resolve_identity(self, info, user_name):
        """Looks up and returns an identity object based on the given user name."""
        query = Identity.join(Actor,
                              Actor.id == Identity.actor_id).select().where(
                                  Identity.user_name == user_name)
        identity_ = await query.gino.load(
            Identity.distinct(
                Identity.id).load(actor=Actor.distinct(Actor.id))).first()

        if identity_ is None:
            raise GraphQLError('Identity does not exist!')

        identity_object = IdentityObjectType(
            display_name=identity_.display_name,
            user_name=identity_.user_name,
            uri=f'{BASE_URL}/u/{identity_.user_name}',
            created=pendulum.now()  # TODO: Get this from the model.
        )

        return identity_object


class Queries(IdentityQuery):
    """Container class for all lamia authentication query classes."""
