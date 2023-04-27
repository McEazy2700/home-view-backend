import strawberry
from homes.graphql.types import CountryType

from homes.models.models import Country

@strawberry.type
class HomesQuery:
    @strawberry.field
    def country(self, id: int) -> CountryType:
        return Country.objects().get(id=id).gql
