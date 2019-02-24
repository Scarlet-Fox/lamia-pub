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
from lamia.activitypub.schema import ActorSchema

ALLOWED_NAME_CHARACTERS_RE = re.compile(r'[a-zA-Z_]+')


class RegisterUser(graphene.Mutation):
    """Register a user account."""
    identity = graphene.Field(lambda: IdentityObjectType)

    class Arguments:
        """Graphene arguments meta class."""
        user_name = graphene.String(
            description=
            'The user name for this new account. Should include only a-z and underscore characters.'
        )
        email_address = graphene.String(
            description='An email address associated with this account.')
        password = graphene.String(
            description='A password with at least 5 characters.')

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

        created_ = pendulum.now().naive()

        actor = ActorSchema()
        actor.id = f'{BASE_URL}/u/{user_name}'
        actor.type = 'Person'
        actor.url = actor.id
        actor.followers = f'{BASE_URL}/u/{user_name}/followers'
        actor.following = f'{BASE_URL}/u/{user_name}/following'
        actor.inbox = f'{BASE_URL}/u/{user_name}/inbox'
        actor.outbox = f'{BASE_URL}/u/{user_name}/outbox'
        actor.name = user_name
        actor.preferredUsername = user_name
        actor_model = actor.to_model()
        actor_model.generate_keys()
        await actor_model.create()

        identity_model = Identity()
        identity_model.actor_id = actor_model.id
        identity_model.display_name = user_name
        identity_model.user_name = user_name
        identity_model.disabled = False
        identity_model.created = created_
        identity_model.last_updated = created_
        await identity_model.create()
        await actor_model.update(identity_id=identity_model.id).apply()

        account_model = Account()
        account_model.email_address = email_address
        account_model.primary_identity_id = identity_model.id
        account_model.created = created_
        account_model.set_password(password)
        await account_model.create()

        new_identity = IdentityObjectType(
            display_name=user_name,
            user_name=user_name,
            uri=f'{BASE_URL}/u/{user_name}',
            avatar='',
            created=account_model.created)

        return RegisterUser(identity=new_identity)


class Mutations(graphene.ObjectType):
    """Container class for all lamia authentication mutations."""
    register_user = RegisterUser.Field(
        description=RegisterUser.mutate.__doc__.replace('\n', ''))
