from typing import List
import strawberry
from homes.graphql.types import CountryType

from homes.models.models import Country

@strawberry.type
class HomesQuery:
    @strawberry.field
    def country(self, id: int) -> CountryType:
        return Country.objects().get(id=id).gql

    @strawberry.field
    def countries(self) -> List[CountryType]:
        return Country.objects().all().bulk_gql
