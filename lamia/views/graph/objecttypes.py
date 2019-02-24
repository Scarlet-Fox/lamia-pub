"""Contains the object types used by the GraphQL API.

While an object type may be linked to a single model, this is not a
requirement. The object types in this file should be created explicitly
for the purpose of being used by GraphQL API queries.

Wherever possible, lamia will take simple approaches to graph structure, for
example - avoiding unchecked recursion, complex queries, and relay. For now,
this is a design decision that is being made for the purpose of maintaining
a predictable approach to database/cache access.

TODO: This file is a work in progress. Fields, classes, and methods will be
added and removed as everything is felt out.

TODO: Add descriptions where needed, once things settle down.
"""
import graphene


class AccountObjectType(graphene.ObjectType):
    """Represents an account."""
    email_address = graphene.String()
    created = graphene.String()


class IdentityObjectType(graphene.ObjectType):
    """An identity represents an actor that is directly attached to an account
    in lamia. A single lamia account may have multiple identities.
    """
    display_name = graphene.String()
    user_name = graphene.String()
    uri = graphene.String()

    avatar = graphene.String()
    created = graphene.DateTime()
