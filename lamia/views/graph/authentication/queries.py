import graphene
from graphql import GraphQLError
from lamia.views.graph.objecttypes import IdentityObjectType
from lamia.models.features import Identity
from lamia.models.activitypub import Actor


class IdentityQuery(graphene.ObjectType):
    """Returns an identity."""
    identity = graphene.Field(lambda: IdentityObjectType)

    async def resolve_identity(self, info, user_name):
        query = Identity.join(Actor,
                              Actor.id == Identity.actor_id).select().where(
                                  Identity.user_name == user_name)
        identity_ = await query.gino.load(
            Identity.distinct(
                Identity.id).load(actor=Actor.distinct(Actor.id))).first()

        if identity_ is None:
            raise GraphQLError()

        loaded_identity = Identity(
            display_name=identity_.user_name,
            user_name=identity_.user_name,
            uri=f'{BASE_URL}/u/identity_',
            created=pendulum.now()  # TODO: Get this from the model.
        )


class Queries(IdentityQuery):
    """Container class for all lamia authentication query classes."""
    pass
