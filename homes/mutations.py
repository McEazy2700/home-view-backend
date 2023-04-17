import strawberry

from homes.models import State, StateType


@strawberry.type
class HomeMutations:
    """
    Contains all mutations for the homes app
    """
    @strawberry.mutation
    def new_state(self, name: str) -> StateType:
        return State.object.new(name).gql()
