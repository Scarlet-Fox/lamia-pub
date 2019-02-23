"""Mutations associated with lamia authentication."""
# pylint: disable=unused-argument
import re
import graphene
import pendulum
from graphql import GraphQLError
from lamia.translation import _
from lamia.config import BASE_URL
from lamia.views.graph.objecttypes import IdentityObjectType
from lamia.models.features import Identity, Account

ALLOWED_NAME_CHARACTERS_RE = re.compile(r'[a-zA-Z_]+')


class RegisterUser(graphene.Mutation):
    """Register a user account."""
    identity = graphene.Field(lambda: IdentityObjectType)

    class Arguments:
        """Graphene arguments meta class."""
        user_name = graphene.String()
        email_address = graphene.String()
        password = graphene.String()

    async def mutate(self, info, user_name, email_address, password):
        """Creates a user account using the given user name, email address,
        and password.
        """
        password = password.strip()
        if len(password) < 5:
            raise GraphQLError(
                _('Password is too short! Should be at least five characters in length.'
                  ))

        if ALLOWED_NAME_CHARACTERS_RE.match(user_name) is None:
            raise GraphQLError(
                _('Invalid user name. Characters allowed are a-z and _.'))

        email_account_used_by = await Account.select('id') \
            .where(Account.email_address == email_address).gino.scalar()
        if not email_account_used_by is None:
            raise GraphQLError(
                _('This email address is already in use for another account.'))

        user_name_used_by = await Identity.select('id') \
            .where(
                (Identity.user_name == user_name) | (Identity.display_name == user_name)
            ).gino.scalar()
        if not user_name_used_by is None:
            raise GraphQLError(
                _('This user name is already in use. User names must be unique.'
                  ))

        new_identity = IdentityObjectType(
            display_name=user_name,
            user_name=user_name,
            uri=f'{BASE_URL}/u/{user_name}',
            avatar='',
            created=pendulum.now()  # TODO: Get this from the model.
        )

        return RegisterUser(identity=new_identity)


class Mutations(graphene.ObjectType):
    """Container class for all lamia authentication mutations."""
    register_user = RegisterUser.Field()
