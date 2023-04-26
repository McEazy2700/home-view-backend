import strawberry
from common.graphql.mutations import CommonMutations
from homes.graphql.mutations import HomeMutations

from homes.graphql.queries import HomesQuery


@strawberry.type
class Query(HomesQuery):
    pass

@strawberry.type
class Mutation(CommonMutations, HomeMutations):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
