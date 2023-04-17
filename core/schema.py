import strawberry
from homes.mutations import HomeMutations

from homes.queries import HomesQuery


@strawberry.type
class Query(HomesQuery):
    pass

@strawberry.type
class Mutation(HomeMutations):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
