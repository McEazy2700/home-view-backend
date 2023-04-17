import strawberry
from typing import List
from .types import Home
from .resolvers import get_homes

@strawberry.type
class HomesQuery:
    homes: List[Home] = strawberry.field(resolver=get_homes)


