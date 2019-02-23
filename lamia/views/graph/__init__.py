"""Roll up all of the queries and mutations for our graph via the magic of
inheritance.
"""
import lamia.views.graph.authentication.mutations as authentication_mutations
import lamia.views.graph.authentication.queries as authentication_queries


class Queries(authentication_queries.Queries):
    """This class is a container for all lamia graph queries."""


class Mutations(authentication_mutations.Mutations):
    """This class is a container for all lamia graph mutations."""
