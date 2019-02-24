"""Roll up all of the queries and mutations for our graph via the magic of
inheritance.
"""
import lamia.views.graph.users.mutations as user_mutations
import lamia.views.graph.users.queries as user_queries


class Queries(user_queries.Queries):
    """This class is a container for all lamia graph queries."""


class Mutations(user_mutations.Mutations):
    """This class is a container for all lamia graph mutations."""
